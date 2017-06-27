Perform project test setup tasks.

This role assumes that Zuul has checked out a change for a project at
``src/{{ zuul.project.canonical_name }}`` and looks for a file named
``tools/test-setup.sh``.  If that file exists and is executable, it will
be run.

This allows projects to specify test-setup steps (such as creating or
initializing a database) in a form that can be easily run by both an
automated testing system and developers.
