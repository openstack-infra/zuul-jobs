Publish contents of ``{{ zuul.executor.work_root }}/artifacts/`` dir using
rsync over ssh to a remote fileserver that has previously been added to
the inventory by :zuul:role:`add-fileserver`.

**Role Variables**

:zuul:role:`add-fileserver` sets the following variable in the hostvars of the
hosts it adds, but it is documented for reference.

.. zuul:rolevar:: zuul_fileserver_project_path

  The remote path. Content will be put into a directory below this path
  that matches ``zuul.project.short_name``. The full path including
  the project short name will be added to the hostvars of the host
  as ``zuul_fileserver_project_path``.
