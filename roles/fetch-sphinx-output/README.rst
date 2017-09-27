Collect output from a sphinx build

By default, this copies the output from the sphinx build on the worker
to the log root of the executor.

**Role Variables**

.. zuul:rolevar:: zuul_executor_dest
   :default: {{ zuul.executor.log_root }}

   The destination directory on the executor.  By default, the log
   root.

.. zuul:rolevar:: sphinx_output_src
   :default: src/{{ zuul.project.canonical_name }}/doc/build/html

   The location on the worker from which to fetch the generated sphinx
   content.  By default, the HTML doc build dir of the current
   project.
