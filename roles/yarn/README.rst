Run yarn command in a source directory. Assumes the appropriate version
of yarn has been installed.

**Role Variables**

.. zuul:rolevar:: yarn_command

   Command to run. If it's a standard lifecycle command, it will be run as
   ``yarn {{ yarn_command }}``. Otherwise it will be run as
   ``yarn run {{ yarn_command }}``.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to run yarn in.
