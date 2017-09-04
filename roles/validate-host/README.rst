Log information about the build node

**Role Variables**

.. zuul:rolevar:: zuul_traceroute_host
   :default: {{ zuul_site_traceroute_host }}

   If defined, a host to run a traceroute against to verify build node
   network connectivity.
   **DEPRECATED** being replaced by zuul_site versions.

.. zuul:rolevar:: zuul_image_manifest
   :default: {{ zuul_site_image_manifest|default('/etc/dib-builddate.txt') }}

   A file expected to be on the filesystem of the build node to read if it
   exists and log. The default value comes from a site-variable called
   ``zuul_site_image_manifest``, but if that is not set
   ``/etc/dib-builddate.txt`` is used, which is written to nodes by
   diskimage-builder in the ``nodepool-base`` element.
   **DEPRECATED** being replaced by zuul_site versions.

.. zuul:rolevar:: zuul_site_traceroute_host

   If defined, a host to run a traceroute against to verify build node
   network connectivity.

.. zuul:rolevar:: zuul_site_image_manifest_files
   :default: ['/etc/dib-builddate.txt', '/etc/image-hostname.txt']

   A list of files to read from the filesystem of the build node and
   whose contents will be logged. The default files are files written
   to nodes by diskimage-builder.
