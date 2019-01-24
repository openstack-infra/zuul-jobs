This is one of a collection of roles which are designed to work
together to build, upload, and promote docker images in a gating
context:

* :zuul:role:`build-docker-image`: Build the images.
* :zuul:role:`upload-docker-image`: Stage the images on dockerhub.
* :zuul:role:`promote-docker-image`: Promote previously uploaded images.

The :zuul:role:`build-docker-image` role is designed to be used in
`check` and `gate` pipelines and simply builds the images.  It can be
used to verify that the build functions, or it can be followed by the
use of subsequent roles to upload the images to Docker Hub.

The :zuul:role:`upload-docker-image` role uploads the images to Docker
Hub, but only with a single tag corresponding to the change ID.  This
role is designed to be used in a job in a `gate` pipeline so that the
build produced by the gate is staged and can later be promoted to
production if the change is successful.

The :zuul:role:`promote-docker-image` role is designed to be used in a
`promote` pipeline.  It requires no nodes and runs very quickly on the
Zuul executor.  It simply re-tags a previously uploaded image for a
change with whatever tags are supplied by
:zuul:rolevar:`build-docker-image.docker_images.tags`.  It also
removes the change ID tag from the repository in Docker Hub, and
removes any similar change ID tags more than 24 hours old.  This keeps
the repository tidy in the case that gated changes fail to merge after
uploading their staged images.

They all accept the same input data, principally a list of
dictionaries representing the images to build.  YAML anchors_ can be
used to supply the same data to all three jobs.

Use the :zuul:role:`install-docker` role to install Docker before
using this role.

**Role Variables**

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   The project directory.  Serves as the base for
   :zuul:rolevar:`build-docker-image.docker_images.context`.

.. zuul:rolevar:: docker_dockerfile
   :default: Dockerfile

   The default Dockerfile name to use. Serves as the base for
   :zuul:rolevar:`build-docker-image.docker_images.dockerfile`.
   This allows a global overriding of Dockerfile name, for example
   when building all images from different folders with similarily
   named dockerfiles.

.. zuul:rolevar:: docker_credentials
   :type: dict

   This is only required for the upload and promote roles.  This is
   expected to be a Zuul Secret with two keys:

   .. zuul:rolevar:: username

      The Docker Hub username.

   .. zuul:rolevar:: password

      The Docker Hub password.

   .. zuul:rolevar:: repository

      Optional; if supplied this is a regular expression which
      restricts to what repositories the image may be uploaded.  The
      following example allows projects to upload images to
      repositories within an organization based on their own names::

        repository: "^myorgname/{{ zuul.project.short_name }}.*"

.. zuul:rolevar:: docker_images
   :type: list

   A list of images to build.  Each item in the list should have:

   .. zuul:rolevar:: context

      The docker build context; this should be a directory underneath
      :zuul:rolevar:`build-docker-image.zuul_work_dir`.

   .. zuul:rolevar:: dockerfile

      The filename of the dockerfile, present in the context folder,
      used for building the image. Provide this if you are using
      a non-standard filename for a specific image.

   .. zuul:rolevar:: repository

      The name of the target repository in dockerhub for the
      image.  Supply this even if the image is not going to be
      uploaded (it will be tagged with this in the local
      registry).

   .. zuul:rolevar:: path

      Optional: the directory that should be passed to docker build.
      Useful for building images with a Dockerfile in the context
      directory but a source repository elsewhere.

   .. zuul:rolevar:: build_args
      :type: list

      Optional: a list of values to pass to the docker ``--build-arg``
      parameter.

   .. zuul:rolevar:: target

      Optional: the target for a multi-stage build.

   .. zuul:rolevar:: tags
      :type: list
      :default: ['latest']

      A list of tags to be added to the image when promoted.

.. _anchors: https://yaml.org/spec/1.2/spec.html#&%20anchor//
