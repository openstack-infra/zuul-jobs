Collect subunit outputs

**Role Variables**

.. zuul:rolevar:: zuul_work_dir
   :default: {{ ansible_user_dir }}/{{ zuul.project.src_dir }}

   Directory to work in. It has to be a fully qualified path.

.. zuul:rolevar:: tox_envlist

   tox environment that was used to run the tests originally.
