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


# TODO(mordred) We should replace this python module with the 'ini' lookup
# module. That runs on the executor, but the executor has a readable copy of
# the setup.cfg for the project in question.
# Just a simple:
#   set_fact:
#     setup_cfg_path: "{{ zuul.executor.work_root }}/"\
#                     "{{ zuul.project.src_dir }}/setup.cfg }}"
#   warning_is_error: "{{ lookup('ini', 'warning[_\_]is[_\-]error section="\
#                     "build_sphinx re=True file=' + setup_cfg_path }}"
#   autodoc_index_modules: "{{ lookup('ini', 'autodoc[_\_]index[_\-]modules"\
#                          "section=build_sphinx re=True file=' + "\
#                          "setup_cfg_path }}"
# should do it. That's a bigger change that we should test aggressively.
def main():
    module = AnsibleModule(
        argument_spec=dict(
            project_dir=dict(required=True, type='str'),
        )
    )
    project_dir = module.params['project_dir']

    warning_is_error = False
    # TODO(mordred) Remove autodoc_index_modules logic  when we get OpenStack
    # projects off of the pbr autoindex
    autodoc_index_modules = False
    autodoc_tree_index_modules = False

    if not os.path.exists(os.path.join(project_dir, 'setup.cfg')):
        module.exit_json(
            changed=False,
            warning_is_error=warning_is_error,
            autodoc_index_modules=autodoc_index_modules,
            msg="No setup.cfg, no action needed")

    try:
        c = configparser.ConfigParser()
        c.read(os.path.join(project_dir, 'setup.cfg'))
    except Exception:
        module.exit_json(
            changed=False,
            warning_is_error=warning_is_error,
            autodoc_index_modules=autodoc_index_modules,
            msg="Error reading setup.cfg, defaulting flags to false")

    if (c.has_section('build_sphinx') and
            c.has_option('build_sphinx', 'warning-is-error')):
        warning_is_error = c.getboolean('build_sphinx', 'warning-is-error')
    if c.has_section('pbr') and c.has_option('pbr', 'autodoc_index_modules'):
        autodoc_index_modules = c.getboolean('pbr', 'autodoc_index_modules')
    if (c.has_section('pbr') and
            c.has_option('pbr', 'autodoc_tree_index_modules')):
        autodoc_tree_index_modules = c.getboolean('pbr',
                                                  'autodoc_tree_index_modules')
    # Set it if either options is set and defer to pbr to figure it out.
    autodoc_index_modules = autodoc_index_modules or autodoc_tree_index_modules
    module.exit_json(
        changed=False,
        warning_is_error=warning_is_error,
        autodoc_index_modules=autodoc_index_modules,
        msg="Doc building options found in setup.cfg")


if __name__ == '__main__':
    main()
