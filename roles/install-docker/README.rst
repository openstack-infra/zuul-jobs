An ansible role to install docker and configure it to use mirrors if available.

**Role Variables**

.. zuul:rolevar:: mirror_fqdn
   :default: {{ zuul_site_mirror_fqdn }}

   The base host for mirror servers.

.. zuul:rolevar:: docker_mirror

   URL to override the generated docker hub mirror url based on
   :zuul:rolevar:`install-docker.mirror_fqdn`.

.. zuul:rolevar:: use_upstream_docker
   :default: True

   By default this role adds repositories to install docker from upstream
   docker. Set this to False to use the docker that comes with the distro.

.. zuul:rolevar:: docker_update_channel
   :default: stable

   Which update channel to use for upstream docker. The two choices are
   ``stable``, which is the default and updates quarterly, and ``edge``
   which updates monthly.

.. zuul:rolevar:: docker_version
   :default: undefined

   Declare this with the version of the docker package to install.
   Undefined will install the latest.  This will look something like
   ``18.06.1~ce~3-0~ubuntu``.  Only supported when using upstream
   docker repos.
