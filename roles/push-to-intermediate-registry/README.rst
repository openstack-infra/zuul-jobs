Push artifacts to the intermediate registry

This role will push any images built by
:zuul:role:`build-docker-image` into an intermediate registry.

Run this in a trusted post-playbook at the end of a job after the
image build.

This requires the :zuul:role:`run-buildset-registry` role already
applied.  It also requires an externally managed "intermediate"
registry operating for the use of Zuul, and it requires "skopeo" to be
installed on the Zuul executors.

**Role Variables**

.. zuul:rolevar:: buildset_registry

   Information about the registry, as returned by
   :zuul:role:`run-buildset-registry`.

   .. zuul:rolevar:: host

      The host (IP address) of the registry.

   .. zuul:rolevar:: port

      The port on which the registry is listening.

   .. zuul:rolevar:: username

      The username used to access the registry via HTTP basic auth.

   .. zuul:rolevar:: password

      The password used to access the registry via HTTP basic auth.

   .. zuul:rolevar:: cert

      The (self-signed) certificate used by the registry.

.. zuul:rolevar:: intermediate_registry

   Information about the registry.  This is expected to be provided as
   a secret.

   .. zuul:rolevar:: host

      The host (IP address) of the registry.

   .. zuul:rolevar:: port

      The port on which the registry is listening.

   .. zuul:rolevar:: username

      The username used to access the registry via HTTP basic auth.

   .. zuul:rolevar:: password

      The password used to access the registry via HTTP basic auth.

.. zuul:rolevar:: docker_images
   :type: list

   A list of images built.  Each item in the list should have:

   .. zuul:rolevar:: repository

      The name of the target repository for the image.

   .. zuul:rolevar:: tags
      :type: list
      :default: ['latest']

      A list of tags to be added to the image.
