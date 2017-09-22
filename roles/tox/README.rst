Runs tox for a project

**Role Variables**

.. zuul:rolevar:: tox_environment

   Environment variables to pass in to the tox run.

.. zuul:rolevar:: tox_envlist
   :default: venv

   Which tox environment to run.

.. zuul:rolevar:: tox_executable
   :default: tox

   Location of the tox executable.

.. zuul:rolevar:: tox_extra_args
   :default: -vv

   String of extra command line options to pass to tox.

.. zuul:rolevar:: tox_constraints_file

   Path to a pip constraints file. Will be provided to tox via
   UPPER_CONSTRAINTS_FILE environment variable if it exists.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to run tox in.
