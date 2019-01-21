This is one of a collection of jobs which are designed to work
together to build, upload, and promote docker images in a gating
context:

  * :zuul:job:`build-docker-image`: Build the images.
  * :zuul:job:`upload-docker-image`: Build and stage the images on dockerhub.
  * :zuul:job:`promote-docker-image`: Promote previously uploaded images.

The :zuul:job:`build-docker-image` job is designed to be used in
a `check` pipeline and simply builds the images to verify that
the build functions.

The :zuul:job:`upload-docker-image` job builds and uploads the images
to Docker Hub, but only with a single tag corresponding to the
change ID.  This job is designed in a `gate` pipeline so that the
build produced by the gate is staged and can later be promoted to
production if the change is successful.

The :zuul:job:`promote-docker-image` job is designed to be used in a
`promote` pipeline.  It requires no nodes and runs very quickly on the
Zuul executor.  It simply re-tags a previously uploaded image for a
change with whatever tags are supplied by
:zuul:jobvar:`build-docker-image.docker_images.tags`.  It also removes
the change ID tag from the repository in Docker Hub, and removes any
similar change ID tags more than 24 hours old.  This keeps the
repository tidy in the case that gated changes fail to merge after
uploading their staged images.

They all accept the same input data, principally a list of
dictionaries representing the images to build.  YAML anchors_ can be
used to supply the same data to all three jobs.

**Job Variables**

.. zuul:jobvar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   The project directory.  Serves as the base for
   :zuul:jobvar:`build-docker-image.docker_images.context`.

.. zuul:jobvar:: docker_images
   :type: list

   A list of images to build.  Each item in the list should have:

   .. zuul:jobvar:: context

      The docker build context; this should be a directory underneath
      :zuul:jobvar:`build-docker-image.zuul_work_dir`.

   .. zuul:jobvar:: repository

      The name of the target repository in dockerhub for the
      image.  Supply this even if the image is not going to be
      uploaded (it will be tagged with this in the local
      registry).

   .. zuul:jobvar:: path

      Optional: the directory that should be passed to docker build.
      Useful for building images with a Dockerfile in the context
      directory but a source repository elsewhere.

   .. zuul:jobvar:: build_args
      :type: list

      Optional: a list of values to pass to the docker ``--build-arg``
      parameter.

   .. zuul:jobvar:: target

      Optional: the target for a multi-stage build.

   .. zuul:jobvar:: tags
      :type: list
      :default: ['latest']

      A list of tags to be added to the image when promoted.

.. _anchors: https://yaml.org/spec/1.2/spec.html#&%20anchor//
