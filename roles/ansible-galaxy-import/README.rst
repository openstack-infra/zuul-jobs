Import ansible roles into ansible galaxy

**Role Variables**

.. zuul:rolevar:: ansible_galaxy_branch
   :default: zuul.branch

   The name of a branch to import.

.. zuul:rolevar:: ansible_galaxy_executable
   :default: ansible-galaxy

   Path to ansible-galaxy executable.

.. zuul:rolevar:: ansible_galaxy_info

   Complex argument which contains the information about the Ansible
   Galaxy server as well as the authentication information needed. It
   is expected that this argument comes from a `Secret`.

  .. zuul:rolevar:: server
     :default: https://galaxy.ansible.com

     The API server destination.

  .. zuul:rolevar:: token

     Identify with github token rather than username and password.
