Run sphinx to generate documentation

**Role Variables**

.. zuul:rolevar:: sphinx_source_dir
   :default: doc/source

   Directory relative to zuul_work_dir that contains the Sphinx sources.

.. zuul:rolevar:: sphinx_build_dir
   :default: doc/build

   Directory relative to zuul_work_dir where build output will be put.

.. zuul:rolevar:: sphinx_builders
   :default: ['html']

   Which sphinx builders to run.

.. zuul:rolevar:: sphinx_warning_is_error

   Whether to treat sphinx build warnings as errors. Defaults to the value of
   ``[build_sphinx] warning-is-error`` in ``setup.cfg`` if defined, ``False``
   if the ``[build_sphinx]`` section is present but the ``warning-is-error``
   option is undefined, or ``True`` if the entire section is undefined.

.. zuul:rolevar:: zuul_work_virtualenv
   :default: ~/.venv

   Virtualenv that sphinx is installed in.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to operate in.
