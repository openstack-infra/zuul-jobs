Collect subunit outputs

**Role Variables**

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to work in

.. zuul:rolevar:: tox_envlist

   tox environment that was used to run the tests originally.
