Installs distro packages using bindep tool

Looks for a ``bindep.txt`` in a project's source directory, or failing
that a ``other-requirements.txt``. If one exists, run ``bindep`` on the
file to produce a list of required distro packages that do not exist and
then install the missing packages.
