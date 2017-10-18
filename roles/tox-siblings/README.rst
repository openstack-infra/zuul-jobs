Installs python packages from other Zuul repos into a tox environment.

**Role Variables**

.. zuul:rolevar:: zuul_workdir
   :default: {{ zuul.project.src_dir }}

   Directory to run tox in.

.. zuul:rolevar:: tox_envlist
   :default: venv

   Which tox environment to run. Defaults to 'venv'.

.. zuul:rolevar:: tox_executable
   :default: tox

   Location of the tox executable. Defaults to 'tox'.

.. zuul:rolevar:: tox_constraints_file

   Path to a pip constraints file. Will be provided to pip via '-c'
   argument for any sibling package installations.

.. zuul:rolevar:: tox_install_siblings
   :default: true

   Flag controlling whether to attempt to install python packages from any
   other source code repos zuul has checked out. Defaults to True.
