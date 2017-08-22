Copy a build-local SSH key to a defined user on all hosts

This role is intended to be run on the Zuul Executor.  It copies a generated
build specific ssh key to a user and adds it to the authorized_keys file of
every host in the inventory.

**Role Variables**

.. zuul:rolevar:: zuul_temp_ssh_key
   :default: "{{ zuul.executor.work_root }}/{{ zuul.build }}_id_rsa"

   Where to source the build private key

.. zuul:rolevar:: copy_sshkey_target_user
   :default: root

   The user to copy the sshkey to.
