Collect output from build nodes

This role collects logs, artifacts and docs from subdirs of the
``zuul_output_dir`` on the remote nodes to equivalent directories
on the executor so that later parts of the system can publish the
content to appropriate permanent locations.

**Role Variables**

.. zuul:rolevar:: zuul_output_dir
   :default: {{ ansible_user_dir }}/zuul-output

   Base directory for collecting job output.
