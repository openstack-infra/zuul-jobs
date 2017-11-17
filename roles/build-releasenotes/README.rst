Build releasenotes for a project, optionally incorporating translations.

**Role Variables**

.. zuul:rolevar:: zuul_work_virtualenv
   :default: ~/.venv

   Virtualenv location in which to install things.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to build releasenotes in.
