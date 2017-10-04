Process test results

Take a testr / stestr repo as input. Produce subunit from the latest
run and the html report using subunit2html.

**Role Variables**

.. zuul:rolevar:: test_results_dir
   :default: None

   The folder where the [s]testr repo lives.

.. zuul:rolevar:: tox_envdir
   :default: venv

   The name of the virtual environemnt created by tox to run tests.
   This may be different from the name of the tox environment.

.. zuul:rolevar:: stage_dir
   :default: {{ ansible_user_dir }}

   Folder into which the output files will be written. Assumption is that
   the user that runs this role has read access to test results and write
   access to tempest_work_dir.

.. zuul:rolevar:: subunit2html
   :default: /usr/os-testr-env/bin/subunit2html

   The full path to subunit2html. This utility is part of os-testr,
   and it's usually baked into test images, hence the default value.

.. zuul:rolevar:: test_results_stage_name
   :default: test_results

   The name of the subunit and html files generated.
