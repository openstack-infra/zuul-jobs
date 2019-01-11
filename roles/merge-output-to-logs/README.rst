Put artifacts and docs into the executor log dir

.. note::

  This role only works in a trusted context. It is intended to
  be used in the post playbook of a base job.

This role moves artifacts and docs into the logs dir when
``zuul.change`` is defined so that they can be uploaded to the
log server for developer preview and validation.

Artifacts and docs are left in place when ``zuul.change`` is
not defined so that normal publication jobs can publish them
to final locations.
