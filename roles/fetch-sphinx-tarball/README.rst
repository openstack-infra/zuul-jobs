Collect output from a sphinx build as a tarball

By default, this copies the output from the sphinx build on the worker
to the log root of the executor as a tarball, and then extracts the
archive into the log root for viewing.

**Role Variables**

.. zuul:rolevar:: sphinx_build_dir
   :default: doc/build

   Directory relative to zuul_work_dir where build output should be
   found.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   The location of the main working directory of the job.
