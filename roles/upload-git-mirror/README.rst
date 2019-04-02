Mirrors a git repository to a remote git server

Meant to be used after a change was successfully merged, this role mirrors a
tested git repository to a remote git server over SSH.

The role assumes that git has been previously installed and does not require
superuser privileges to run.

**Role Variables**

.. zuul:rolevar:: git_mirror_credentials

   Dictionary that provides the remote git repository credentials

  .. zuul:rolevar:: user

     SSH user for the remote git repository

  .. zuul:rolevar:: host

     SSH host for the remote git repository

  .. zuul:rolevar:: ssh_key

     Literal private key contents.
     Should start with something like ``-----BEGIN RSA PRIVATE KEY-----``.

  .. zuul:rolevar:: host_key

     SSH host key of the remote git server.
     Can be obtained with ``ssh-keyscan -H <host>``.

.. zuul:rolevar:: git_mirror_repository

   Path of the remote git repository
