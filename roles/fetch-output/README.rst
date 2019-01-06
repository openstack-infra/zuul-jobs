Collect output from build nodes

This role collects logs, artifacts and docs from subdirs of the
``zuul_output_dir`` on the remote nodes to equivalent directories
on the executor so that later parts of the system can publish the
content to appropriate permanent locations.

.. note::

  Log content for multi-node jobs will be put into subdirectories
  based on remote node name. It is expected that artifacts and docs
  produced be inherently unique regardless of which build node they
  were produced on, so all artifacts and docs are pulled back to
  the same artifacts and docs directory.

**Role Variables**

.. zuul:rolevar:: zuul_output_dir
   :default: {{ ansible_user_dir }}/zuul-output

   Base directory for collecting job output.
