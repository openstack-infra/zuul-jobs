Log the inventory used to run the job to the job's log dir.

This will result in the log collection roles logging the job inventory.

**Role Variables**

.. zuul:rolevar:: zuul_info_dir
   :default: {{ zuul.executor.log_root }}/zuul-info

   The directory path to store the inventory file.
