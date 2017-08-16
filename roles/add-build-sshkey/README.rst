Generate and install a build-local SSH key on all hosts

This role is intended to be run on the Zuul Executor at the start of
every job.  It generates an SSH keypair and installs the public key in
the authorized_keys file of every host in the inventory.  It then
removes all keys from this job's SSH agent so that the original key
used to log into all of the hosts is no longer accessible, then adds
the newly generated private key.

**Role Variables**

.. zuul:rolevar:: zuul_temp_ssh_key

   Where to put the newly-generated SSH private key.
