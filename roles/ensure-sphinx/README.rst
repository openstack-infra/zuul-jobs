Ensure sphinx is installed

Installs sphinx. Also installs any dependencies needed in the first of
doc/requirements.txt and test-requirements.txt to be found.

All pip installs are done with a provided constraints file, if given.

**Role Variables**

.. zuul:rolevar:: constraints_file

   Optional path to a pip constraints file for installing python libraries.

.. zuul:rolevar:: doc_building_packages
   :default: ['sphinx']

   List of python packages to install for building docs.

.. zuul:rolevar:: zuul_work_virtualenv
   :default: ~/.venv

   Virtualenv location in which to install things.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to operate in.
