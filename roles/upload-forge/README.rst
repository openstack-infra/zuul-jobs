Upload puppet module tarball to a Forge server

This role requires the python requests module to be
installed where Ansible is executing this role.

**Role Variables**

  .. zuul:rolevar:: forge_url
     :default: https://forgeapi.puppet.com

     The URL to the Puppet Forge API.

  .. zuul:rolevar:: forge_username

     Username to use to log in to Puppet Forge.

  .. zuul:rolevar:: forge_password

     Password to use to log in to Puppet Forge.

  .. zuul:rolevar:: forge_tarball

     Absolute path to the module tarball that should be
     uploaded.
