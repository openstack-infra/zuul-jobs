Have ARA generate html logs if ARA and ARA data are both present.

**Role Variables**

.. zuul:rolevar:: ara_compress_html

   Whether to compress the ARA HTML output or not.
   Defaults to ``true``.

.. tip::
   Make sure the web server is configured to set the required mimetypes_ in
   order to serve gzipped content properly.

.. _mimetypes: https://git.openstack.org/cgit/openstack-infra/puppet-openstackci/tree/templates/logs.vhost.erb?id=5fe1f3d2d5e40c2458721e7dcf8631d62ea2525f#n24
