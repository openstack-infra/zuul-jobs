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
