Upload logs to a static webserver

This uploads logs to a static webserver using SSH.

**Role Variables**

.. zuul:rolevar:: zuul_log_url

   Base URL where logs are to be found.

.. zuul:rolevar:: zuul_logserver_root
   :default: /srv/static/logs

   The root path to the logs on the logserver.
