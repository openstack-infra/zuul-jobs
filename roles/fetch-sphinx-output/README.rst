Collect output from a sphinx build

By default, this copies the output from the sphinx build on the worker
to the log root of the executor.

**Role Variables**

.. zuul:rolevar:: zuul_executor_dest
   :default: {{ zuul.executor.log_root }}

   The destination directory on the executor.  By default, the log
   root.

.. zuul:rolevar:: sphinx_build_dir
   :default: doc/build

   Directory relative to zuul_work_dir where build output will be put.

.. zuul:rolevar:: sphinx_output_src
   :default: {{ zuul_work_dir }}/{{ sphinx_build_dir }}/html

   The location on the worker from which to fetch the generated sphinx
   content.  By default, the HTML doc build dir of the current
   project.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   The location of the main working directory of the job.
