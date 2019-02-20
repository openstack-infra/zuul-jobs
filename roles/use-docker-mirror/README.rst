Configure docker to use mirrors if available.

**Role Variables**

.. zuul:rolevar:: mirror_fqdn
   :default: {{ zuul_site_mirror_fqdn }}

   The base host for mirror servers.

.. zuul:rolevar:: docker_mirror

   URL to override the generated docker hub mirror url based on
   :zuul:rolevar:`install-docker.mirror_fqdn`.

.. zuul:rolevar:: docker_insecure_registries
   :default: undefined

   Declare this with a list of insecure registries to define the
   registries which are allowed to communicate with HTTP only or
   HTTPS with no valid certificate.
