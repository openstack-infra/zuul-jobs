Run npm command in a source directory. Assumes the appropriate version
of npm has been installed.

**Role Variables**

.. zuul:rolevar:: npm_command

   Command to run. If it's a standard npm lifecycle command, it will be run as
   ``npm {{ npm_command }}``. Otherwise it will be run as
   ``npm run {{ npm_command }}``.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to run npm in.
