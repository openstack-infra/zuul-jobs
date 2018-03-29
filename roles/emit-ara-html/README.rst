**THIS ROLE IS DEPRECATED**, please use the ``ara-report`` role instead.
``ara-report`` provides the same default behavior with the generation of a HTML
report and provides additional functionality that can be used to dynamically
load databases for improved performance and scalability.

Have ARA generate html logs if ARA and ARA data are both present.

**Role Variables**

.. zuul:rolevar:: ara_generate_html

   Whether to generate a static ARA HTML report or not.
   Possible values:

   - ``true`` (always generate a report)
   - ``false`` (never generate a report)
   - ``failure`` (only generate a report on failure)

   Defaults to ``true``.

.. zuul:rolevar:: ara_compress_html

   Whether to compress the ARA HTML output or not.
   Defaults to ``true``.

.. zuul:rolevar:: ara_save_database

   Whether the ARA sqlite database should be saved as part of the logs.
   Defaults to ``false``.

.. tip::
   Make sure the web server is configured to set the required mimetypes_ in
   order to serve gzipped content properly.

.. _mimetypes: https://git.openstack.org/cgit/openstack-infra/puppet-openstackci/tree/templates/logs.vhost.erb?id=5fe1f3d2d5e40c2458721e7dcf8631d62ea2525f#n24
