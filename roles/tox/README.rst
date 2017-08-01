Runs tox for a project.

Role Variables

tox_environment
  Environment variables to pass in to the tox run.

tox_environment_defaults
  Default environment variables to pass in to the tox run. Intended to allow
  setting a set of environment variables in a base job but to still allow
  specific settings on a per-job or per-variant basis.

tox_envlist
  Which tox environment to run. Defaults to 'venv'.

tox_executable
  Location of the tox executable. Defaults to 'tox'.

tox_extra_args
  String of extra command line options to pass to tox. Defaults to '-vv'.

zuul_work_dir
  Directory to run tox in.
