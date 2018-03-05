An ansible role to configure services to use mirrors.

**Role Variables**

.. zuul:rolevar:: mirror_fqdn
   :default: {{ zuul_site_mirror_fqdn }}

   The base host for mirror servers.

.. zuul:rolevar:: pypi_mirror

   URL to override the generated pypi mirror url based on
   :zuul:rolevar:`configure-mirrors.mirror_fqdn`.

.. zuul:rolevar:: set_apt_mirrors_trusted
   :default: False

   Set to True in order to tag APT mirrors as trusted, needed
   when accessing unsigned mirrors with newer releases like
   Ubuntu Bionic.
