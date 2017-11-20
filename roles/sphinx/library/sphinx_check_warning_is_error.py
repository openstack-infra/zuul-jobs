#!/usr/bin/python

# Copyright (c) 2017 Red Hat
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: sphinx_check_warning_is_error
short_description: Read the warning-is-error setting from setup.cfg
author: Monty Taylor (@mordred)
description:
  - When running sphinx using sphinx-build and not using python setup.py
    build_sphinx there is no way to set warning-is-error in a config file.
    The sphinx-build command expects the -W flag to be passed. Read the setting
    from a setup.cfg file if one exists.
requirements:
  - "python >= 3.5"
options:
  project_dir:
    description:
      - The directory in which the project we care about is in.
    required: true
    type: str
'''

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import os

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            project_dir=dict(required=True, type='str'),
        )
    )
    project_dir = module.params['project_dir']

    if not os.path.exists(os.path.join(project_dir, 'setup.cfg')):
        module.exit_json(
            changed=False,
            warning_is_error=False,
            msg="No setup.cfg, no action needed")

    try:
        c = configparser.ConfigParser()
        c.read(os.path.join(project_dir, 'setup.cfg'))
        warning_is_error = c.getboolean('build_sphinx', 'warning-is-error')
    except Exception:
        module.exit_json(
            changed=False,
            warning_is_error=False,
            msg="Setting not found in setup.cfg, defaulting to false")
    module.exit_json(
        changed=False,
        warning_is_error=warning_is_error,
        msg="warning_is_error setting found in build_sphinx section")


if __name__ == '__main__':
    main()
