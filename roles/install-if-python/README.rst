Install the contents of a directory if they contain a python project.

Installs into a virtualenv.

**Role Variables**

.. zuul:rolevar:: install_package
   :default: true

   Flag indicating whether or not the software in the ``zuul_work_dir`` should
   be installed.

.. zuul:rolevar:: error_on_failure

   Flag that indicates installation errors should result in failure. Failures
   in installing the target directory are ignored by default.

.. zuul:rolevar:: constraints_file

   Optional path to a pip constraints file to use when installing.

.. zuul:rolevar:: zuul_work_virtualenv
   :default: ~/.venv

   Virtualenv location in which to install things.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to operate in.
