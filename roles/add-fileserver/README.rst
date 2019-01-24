Add a remote fileserver to the inventory so that content can be uploaded
in subsequent tasks or roles.

**Role Variables**

.. zuul:rolevar:: fileserver

   Complex argument which contains the information about the remote
   destination as well as the authentication information needed. It is
   expected that this argument comes from a `Secret
   <https://zuul-ci.org/docs/zuul/user/config.html#secret>`_

   Example:

   .. code-block:: yaml

      - secret:
          name: site_logs
            data:
              fqdn: logs.example.org
              path: /srv/static/logs
              ssh_known_hosts: |
                logs.example.org ssh-rsa ...
              ssh_username: zuul
              ssh_private_key: !encrypted/pkcs1-oaep
                - ...

   .. zuul:rolevar:: fqdn

      The FQDN of the remote host.

   .. zuul:rolevar:: path

      The remote path. Content will be put into a directory below this path
      that matches ``zuul.project.short_name``. The full path including
      the project short name will be added to the hostvars of the host
      as ``zuul_fileserver_project_path``.

   .. zuul:rolevar:: ssh_known_hosts

      String containing known host signature for the remote host.

   .. zuul:rolevar:: ssh_private_key

      Contents of the ssh private key to use.

   .. zuul:rolevar:: ssh_username
      :default: ansible_user

      Remote ssh user name to use.

.. zuul:rolevar:: fileserver_leading_path

   This is an optional variable that will be inserted between the base
   of the path (provided by the `path` variable) and the
   ``zuul.project.short_name`` final path element.
