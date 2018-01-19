Install SSH public key(s) on all hosts

This role is intended to be run at the end of a failed job for which the build
node set will be held with zuul's `autohold` command.

It copies the public key(s) into the authorized_keys file of every host in the
inventory, allowing privileged users to access the node set for debugging or
post-mortem analysis.

Add this stanza at the end of your project's base post playbook to activate this
functionality:

.. code-block:: yaml

   - hosts: all
     roles:
       - role: add-authorized-keys
         public_keys:
           - public_key: ssh-rsa AAAAB... venkman@parapsy.columbia.edu
           - public_key: ssh-rsa AAAAB... spengler@parapsy.columbia.edu
         when: not zuul_success | bool

.. caution::
   Including this role earlier in any playbook may allow the keys' owners to
   tamper with the execution of the jobs. It is strongly advised against doing
   so.

**Role Variables**

.. zuul:rolevar:: ssh_public_keys

  A list of keys to inject.

  .. zuul:rolevar:: public_key

    A public key to inject into authorized_keys, or a URL to a public key.
