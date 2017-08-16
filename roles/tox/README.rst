Runs tox for a project

**Role Variables**

.. zuul:rolevar:: tox_environment

   Environment variables to pass in to the tox run.

.. zuul:rolevar:: tox_environment_defaults

   Default environment variables to pass in to the tox run. Intended
   to allow setting a set of environment variables in a base job but
   to still allow specific settings on a per-job or per-variant basis.

.. zuul:rolevar:: tox_envlist
   :default: venv

   Which tox environment to run.

.. zuul:rolevar:: tox_executable
   :default: tox

   Location of the tox executable.

.. zuul:rolevar:: tox_extra_args
   :default: -vv

   String of extra command line options to pass to tox.

.. zuul:rolevar:: zuul_work_dir
   :default: src/{{ zuul.project.canonical_name }}

   Directory to run tox in.
