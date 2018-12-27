Upload puppet module to Puppet Forge

**Role Variables**

  .. zuul:rolevar:: puppet_module_dir
     :default: {{ zuul.project.src_dir }}

     The folder where the puppet module code is that it can
     switch folder to.

  .. zuul:rolevar:: blacksmith_forge_url
     :default: https://forgeapi.puppetlabs.com

     The URL to the Puppet Forge API.

  .. zuul:rolevar:: blacksmith_forge_username

     Username to use to log in to Puppet Forge.

  .. zuul:rolevar:: blacksmith_forge_password

     Password to use to log in to Puppet Forge.
