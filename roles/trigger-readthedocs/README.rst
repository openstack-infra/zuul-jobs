Trigger readthedocs build for a project

**Role Variables**

.. zuul:rolevar:: rtd_project_name
   :default: ``{{ zuul.project.short_name }}``

   The readthedocs project name

.. zuul:rolevar:: rtd_webhook_id

   The readthedocs webhook API ID.  This needs to be taken from the
   project's "Integrations" dashboard page in RTD.  The URL will look
   like ``readthedocs.org/api/v2/webhook/<project-name>/<id>/``.

   This may come from a secret, however it can not be triggered
   without authentication.

.. zuul:rolevar:: rtd_integration_token

   The webhook integration token.  You'll find this value on the
   project's "Integrations" dashboard page in RTD.  This is expected
   to come from a secret.  This can be used instead of
   username/password combo.

.. zuul:rolevar:: rtd_username

   The readthedocs username.  If set, this will be used to
   authenticate in preference to any token set via
   ``rtd_integration_token``.

.. zuul:rolevar:: rtd_password

   Password for ``rtd_username``.  Must be set if password is set.
   This is expected to come from a secret.
