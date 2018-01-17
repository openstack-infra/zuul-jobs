Collect output from a coverage run

By default, this copies the output from a coverage run
on the worker to the log root of the executor.

**Role Variables**

.. zuul:rolevar:: zuul_executor_dest
   :default: {{ zuul.executor.log_root }}

   The destination directory on the executor.  By default, the log
   root.

.. zuul:rolevar:: coverage_output_src
   :default: {{ zuul.project.src_dir }}/cover/

   The location on the worker from which to fetch the coverage
   output detail.  By default, the ``cover`` dir of the current
   project.

