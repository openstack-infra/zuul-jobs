Log information about the build node

**Role Variables**

.. zuul:rolevar:: zuul_site_traceroute_host

   If defined, a host to run a traceroute against to verify build node
   network connectivity.

.. zuul:rolevar:: zuul_site_image_manifest_files
   :default: ['/etc/dib-builddate.txt', '/etc/image-hostname.txt']

   A list of files to read from the filesystem of the build node and
   whose contents will be logged. The default files are files written
   to nodes by diskimage-builder.
