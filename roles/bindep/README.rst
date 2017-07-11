Installs distro packages using bindep tool

Looks for a ``bindep.txt`` in a project's source directory, or failing
that a ``other-requirements.txt``. If one exists, run ``bindep`` on the
file to produce a list of required distro packages that do not exist and
then install the missing packages.

Role Variables

bindep_dir
  The directory to look for bindep files in. Defaults to current directory.

bindep_profile
  A specific bindep profile to request. Defaults to empty.

bindep_file
  Path to a specific bindep file to read from.

bindep_command
  Path to the bindep command. Defaults to unset which will look for a system
  installed bindep. If bindep_command is not found, bindep will be installed
  into a temporary virtualenv.

bindep_fallback
  Path to a bindep fallback file to be used if no bindep file can be found in
  `bindep_dir`.
