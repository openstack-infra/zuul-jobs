An ansible role to configure services to use mirrors.

Role Variables

mirror_host
  The base host for mirror servers

mirror_domain
  Domain of the mirror. Use in pydistutils to allow find-links arguments to
  be used if they point at this domain.

pypi_mirror
  URL to override the generated pypi mirror url based on mirror_host
