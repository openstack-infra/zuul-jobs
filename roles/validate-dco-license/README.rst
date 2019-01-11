Validate all commits have Signed-off-by header

**Role Variables**

.. zuul:rolevar:: dco_license_failure

   Message to display when Signed-off-by header is missing.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to DCO license check in.
