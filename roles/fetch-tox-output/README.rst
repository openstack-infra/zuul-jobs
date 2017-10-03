Collect log output from a tox build

**Role Variables**

.. zuul:rolevar:: tox_envlist
   :default: venv

   Which tox environment to fetch log output from.

.. zuul:rolevar:: tox_executable
   :default: tox

   Location of the tox executable.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory tox was run in.
