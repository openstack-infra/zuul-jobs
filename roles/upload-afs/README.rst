Copy contents from ``{{ zuul.executor.work_root }}/artifacts/`` to AFS

**Role Variables**

.. zuul:rolevar:: afs_source

  Path to local source directory.

.. zuul:rolevar:: afs_target

  Target path in AFS (should begin with '/afs/...').
