Container Images
================

This repo has several jobs which can form the basis of a system
supporting a full gating process for continuously deployed container
images.  They can be used to build or test images which rely on other
images using the full power of Zuul's speculative execution.

In order to use these jobs to their full potential, the Zuul site
administrator will need to run a simple but dedicated container image
registry, and define local versions of the jobs to use it.  The
following sections describe how to define those jobs and how the
system is intended to work once the jobs are defined.

Run an Intermediate Container Registry
--------------------------------------

A dedicated container registry is required for the use of these jobs.
It is merely used to temporarily hold images so that they can be
transferred between jobs running in different projects at different
times.  It does not need to be publicly accessible or particularly
robust.  If its backing storage fails and needs to be replaced, the
only result is that some jobs running in Zuul may fail and may need to
be re-run.  In this system, it is called the "intermediate registry"
to distinguish it from other registry services.

You may run the registry in whatever manner is appropriate for your
site.  The following docker-compose file may be used as an example
of a working deployment suitable for production:

.. code-block:: yaml

   services:
     registry:
       restart: always
       image: registry:2
       network_mode: host
       environment:
         REGISTRY_HTTP_TLS_CERTIFICATE: /certs/domain.crt
         REGISTRY_HTTP_TLS_KEY: /certs/domain.key
         REGISTRY_AUTH: htpasswd
         REGISTRY_AUTH_HTPASSWD_PATH: /auth/htpasswd
         REGISTRY_AUTH_HTPASSWD_REALM: Registry Realm
       volumes:
         - /var/registry/data:/var/lib/registry
         - /var/registry/certs:/certs
         - /var/registry/auth:/auth

You will need to provide the SSL certificate and key values, as well
as the htpassword file with a user and password already present.

Once that service is running, create the following four jobs in a
Zuul config-project:

.. _yoursite-buildset-registry:

yoursite-buildset-registry
~~~~~~~~~~~~~~~~~~~~~~~~~~

This job is used to provide a temporary "buildset registry" to jobs
running in your system; it communicates with the "intermediate"
registry described above.

.. code-block:: yaml
   :caption: zuul.yaml

   - secret:
       name: yoursite-intermediate-registry
       data:
         host: insecure-ci-registry.example.org
         port: 5000
         username: zuul
         password: !encrypted/pkcs1-oaep
           - ...

   - job:
       name: yoursite-buildset-registry
       pre-run: playbooks/buildset-registry/pre.yaml
       run: playbooks/buildset-registry/run.yaml
       post-run: playbooks/buildset-registry/post.yaml
       secrets:
         - secret: yoursite-intermediate-registry
           name: intermediate_registry
       requires: docker-image

The credentials in the secret should match those you supplied when
creating the intermediate registry.

The ``requires: docker-image`` attribute means that whenever this job
(or any jobs which inherit from it) run, Zuul will search ahead of the
change in the dependency graph to find any jobs which produce
docker-images and tell this job about them.  This allows the job to
pull images from the intermediate registry into the buildset registry.

.. code-block:: yaml
   :caption: playbooks/buildset-registry/pre.yaml

   - hosts: all
     tasks:
       - name: Install docker
         include_role:
           name: install-docker
       - name: Run buildset registry (if not already running)
         when: buildset_registry is not defined
         include_role:
           name: run-buildset-registry
       - name: Use buildset registry
         include_role:
           name: use-buildset-registry

   - hosts: localhost
     roles:
       - pull-from-intermediate-registry

This playbook runs a buildset registry if one isn't already running.
It returns the connection information back to Zuul in a variable
called ``buildset_registry``.  Other jobs will use that to learn how
to connect to the registry, and we can use that here to find out if
one was already started in a previous job.  We will use that facility
in the :ref:`yoursite-build-docker-image` job below.

.. code-block:: yaml
   :caption: playbooks/buildset-registry/run.yaml

   - hosts: localhost
     tasks:
       - name: Pause the job
         zuul_return:
           data:
             zuul:
               pause: true

The ``pause`` causes the job to wait until all jobs which depend on
this one are completed.

.. code-block:: yaml
   :caption: playbooks/buildset-registry/post.yaml

   - hosts: localhost
     roles:
       - push-to-intermediate-registry

.. _yoursite-build-docker-image:

yoursite-build-docker-image
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This job builds one or more docker images and interacts with the
buildset and intermediate registries.

.. code-block:: yaml
   :caption: zuul.yaml

   - job:
       name: yoursite-build-docker-image
       parent: yoursite-buildset-registry
       run: playbooks/docker-image/run.yaml
       provides: docker-image

Note that the parent of this job is :ref:`yoursite-buildset-registry`.
This means that a simple repo that only needs to support one image
building job and doesn't have any other jobs which require a buildset
registry can just add this job alone and it will run a buildset
registry on the build host.  More complex scenarios would run the
:ref:`yoursite-buildset-registry` job on its own and construct a job
graph that depends on it.  Because the pre-run playbook in the
buildset-registry job only runs a buildset registry if one isn't
already running, it can be used for both cases.  And because the run
playbook which pauses the job is overridden in this job, this job will
not pause.

.. code-block:: yaml
   :caption: playbooks/docker-image/run.yaml

   - hosts: all
     roles:
       - build-docker-image

.. _yoursite-upload-docker-image:

yoursite-upload-docker-image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This job further builds on the :ref:`yoursite-build-docker-image` job
and additionally uploads the image to Docker Hub.  Depending on the
situation, you could encode the Docker Hub credentials into this job
as a secret, or you could allow other users to provide them via the
`pass-to-parent <https://zuul-ci.org/docs/zuul/user/config.html#attr-job.secrets.pass-to-parent>`_ feature of secrets.

.. code-block:: yaml
   :caption: zuul.yaml

   - job:
       name: yoursite-upload-docker-image
       parent: yoursite-build-docker-image
       post-run: playbooks/docker-image/upload.yaml

.. code-block:: yaml
   :caption: playbooks/docker-image/upload.yaml

   - hosts: all
     roles:
       - upload-docker-image

.. _yoursite-promote-docker-image:

yoursite-promote-docker-image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This job does nothing that the :zuul:job:`promote-docker-image` job in
this repo doesn't already do, but since you created local versions of
the other two jobs, you should make one of this as well for
consistency.  If you chose to add Docker Hub credentials to the
:ref:`yoursite-upload-docker-image` job, you should do that here as
well.

.. code-block:: yaml
   :caption: zuul.yaml

   - job:
       name: yoursite-promote-docker-image
       parent: promote-docker-image

System Architecture
-------------------

Now that those jobs are defined, this section describes how they work
together.

There are a few key concepts to keep in mind:

A *buildset* is a group of jobs all running on the same change.

A *buildset registry* is a container image registry which is used to
store speculatively built images for the use of jobs in a single
buildset.  It holds the differences between the current state of the
world and the future state if the change in question (and all of its
dependent changes) were to merge.  It must be started by one of the
jobs in a buildset, and it ceases to exist once that job is complete.

An *intermediate registry* is a long-running registry that is used to
store images created for unmerged changes for use by other unmerged
changes.  It is not publicly accessible and is intended only to be
used by Zuul in order to transfer artifacts from one buildset to
another.

With these concepts in mind, the jobs described above implement the
following workflow for a single change:

.. _buildset_image_transfer:

.. seqdiag::
   :caption: Buildset registry image transfer

   seqdiag image_transfer {
     Ireg [label="Intermediate\nRegistry"];
     Breg [label="Buildset\nRegistry"];
     Bjob [label="Image Build Job"];
     Djob [label="Deployment Test Job"];

     Ireg -> Breg [label='Images from previous changes'];
     Breg -> Bjob [label='Images from previous changes'];
     Breg <- Bjob [label='Current image'];
     Ireg <- Breg [noactivate, label='Current image'];
     Breg -> Djob [label='Current and previous images'];
     Breg <- Djob [style=none];
     Ireg <- Breg [style=none];
   }

The intermediate registry is always running and the buildset registry
is started by a job running on a change.  The "Image Build" and
"Deployment Test" jobs are example jobs which might be running on a
change.  Essentially, these are image producer or consumer jobs
respectively.

There are two ways to use the jobs described above:

A Repository with Producers and Consumers
-----------------------------------------

The first is in a repository where images are both produced and
consumed.  In this case, we can expect that there will be at least one
image build job, and at least one job which uses that image (for
example, by performing a test deployment of the image).  In this case
we need to construct a job graph with dependencies as follows:

.. blockdiag::

   blockdiag dependencies {
     obr [label='yoursite-\nbuildset-registry'];
     bi [label='build-image'];
     ti [label='test-image'];

     obr <- bi <- ti;
   }

The :ref:`yoursite-buildset-registry` job will run first and
automatically start a buildset registry populated with images built
from any changes which appear ahead of the current change.  It will
then return its connection information to Zuul and pause and continue
running until the completion of the build and test jobs.

The build-image job should inherit from
:ref:`yoursite-build-docker-image`, which will ensure that it is
automatically configured to use the buildset registry.

The test-image job is something that you will create yourself.  There
is no standard way to test or deploy an image, that depends on your
application.  However, there is one thing you will need to do in your
job to take advantage of the buildset registry.  In a pre-run playbook,
use the `use-buildset-registry
<https://zuul-ci.org/docs/zuul-jobs/roles.html#role-use-buildset-registry>`_
role:

.. code-block:: yaml

   - hosts: all
     roles:
       - use-buildset-registry

That will configure the docker daemon on the host to use the buildset
registry so that it will use the newly built version of any required
images.

A Repository with Only Producers
--------------------------------

The second way to use these jobs is in a repository where an image is
merely built, but not deployed.  In this case, there are no consumers
of the buildset registry other than the image build job, and so the
registry can be run on the job itself.  In this case, you may omit the
:ref:`yoursite-buildset-registry` job and run only the
:ref:`yoursite-build-docker-image` job.

Publishing an Image
-------------------

So far we've covered the image building process.  This system also
provides two more jobs that are used in publishing images to Docker
Hub.

The :ref:`yoursite-upload-docker-image` job does everything the
:ref:`yoursite-build-docker-image` job does, but it also uploads
the built image to Docker Hub using an automatically-generated and
temporary tag.  The "build" job is designed to be used in the
*check* pipeline, while the "upload" job is designed to take its
place in the *gate* pipeline.  By front-loading the upload to Docker
Hub, we reduce the chance that a credential or network error will
prevent us from publishing an image after a change lands.

The :ref:`yoursite-promote-docker-image` job is designed to be
used in the *promote* pipeline and simply re-tags the image on Docker
Hub after the change lands.

Keeping in mind that everything described above in
:ref:`buildset_image_transfer` applies to the
:ref:`yoursite-upload-docker-image` job, the following illustrates
the additional tasks performed by the "upload" and "promote" jobs:

.. seqdiag::

   seqdiag image_transfer {
     DH [activated, label="Docker Hub"];
     Ujob [label="upload-image"];
     Pjob [label="promote-image"];

     DH -> Ujob [style=none];
     DH <- Ujob [label='Current image with temporary tag'];
     DH -> Pjob [label='Current image manifest with temporary tag',
                 note='Only the manifest
                       is transferred,
                       not the actual
                       image layers.'];
     DH <- Pjob [label='Current image manifest with final tag'];
   }
