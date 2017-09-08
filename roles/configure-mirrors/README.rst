An ansible role to configure services to use mirrors.

**Role Variables**

.. zuul:rolevar:: mirror_fqdn
   :default: {{ zuul_site_mirror_fqdn }}

   The base host for mirror servers.

.. zuul:rolevar:: pypi_mirror

   URL to override the generated pypi mirror url based on
   :zuul:rolevar:`configure-mirrors.mirror_fqdn`.
