Install yarn from yarnpkg repos

**Role Variables**

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   The directory to work in.

.. zuul:rolevar:: yarn_lock_file_path
   :default: {{ zuul_work_dir }}/yarn.lock

   Path to yarn.lock file used by a project.
