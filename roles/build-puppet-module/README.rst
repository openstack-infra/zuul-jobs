An ansible role to build a Puppet module.  This role assumes that Puppet is
already installed on the target system (either manually or using bindep).

**Role Variables**

.. zuul:rolevar:: puppet_module_chdir
   :default: {{ zuul.project.src_dir }}

   The folder to switch into in order to build the Puppet module
