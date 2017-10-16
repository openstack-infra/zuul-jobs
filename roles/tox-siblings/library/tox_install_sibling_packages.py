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
module: tox_install_sibling_packages
short_description: Install packages needed by tox that have local git versions
author: Monty Taylor (@mordred)
description:
  - Looks for git repositories that zuul has placed on the system that provide
    python packages needed by package tox is testing. If if finds any, it will
    install them into the tox virtualenv so that subsequent runs of tox will
    use the provided git versions.
requirements:
  - "python >= 3.5"
options:
  tox_envlist:
    description:
      - The tox environment to operate in.
    required: true
    type: str
  project_dir:
    description:
      - The directory in which the project we care about is in.
    required: true
    type: str
  projects:
    description:
      - A list of project dicts that zuul knows about
    required: true
    type: list
'''

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import os
import pip
import subprocess
import tempfile

from ansible.module_utils.basic import AnsibleModule


def get_sibling_python_packages(projects):
    '''Finds all python packages that zuul has cloned.

    If someone does a require_project: and then runs a tox job, it can be
    assumed that what they want to do is to test the two together.
    '''
    packages = {}

    for project in projects:
        root = project['src_dir']
        setup_cfg = os.path.join(root, 'setup.cfg')
        if os.path.exists(setup_cfg):
            c = configparser.ConfigParser()
            c.read(setup_cfg)
            package_name = c.get('metadata', 'name')
            packages[package_name] = root
    return packages


def get_installed_packages(tox_python):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_requirements:
        tmp_requirements.write(subprocess.check_output(
            [tox_python, '-m', 'pip', 'freeze']))
        tmp_requirements.file.flush()
        return pip.req.req_file.parse_requirements(
            tmp_requirements.name, session=pip.download.PipSession())


def main():
    module = AnsibleModule(
        argument_spec=dict(
            tox_envlist=dict(required=True, type='str'),
            project_dir=dict(required=True, type='str'),
            projects=dict(required=True, type='list'),
        )
    )
    envlist = module.params['tox_envlist']
    project_dir = module.params['project_dir']
    projects = module.params['projects']

    if not os.path.exists(os.path.join(project_dir, 'setup.cfg')):
        module.exit_json(changed=False, msg="No setup.cfg, no action needed")

    # Who are we?
    try:
        c = configparser.ConfigParser()
        c.read(os.path.join(project_dir, 'setup.cfg'))
        package_name = c.get('metadata', 'name')
    except Exception:
        module.exit_json(
            changed=False, msg="No name in setup.cfg, skipping siblings")

    envdir = '{project_dir}/.tox/{envlist}'.format(
        project_dir=project_dir, envlist=envlist)
    if not os.path.exists(envdir):
        module.exit_json(
            changed=False, msg="envdir does not exist, skipping siblings")

    tox_python = '{envdir}/bin/python'.format(envdir=envdir)
    # Write a log file into the .tox dir so that it'll get picked up
    # Name it with envlist as a prefix so that fetch-tox-output will properly
    # get it in a multi-env scenario
    log_dir = '{envdir}/log'.format(envdir=envdir)
    log_file = '{log_dir}/{envlist}-siblings.txt'.format(
        log_dir=log_dir, envlist=envlist)

    log = list()
    log.append(
        "Processing siblings for {name} from {project_dir}".format(
            name=package_name,
            project_dir=project_dir))

    changed = False

    sibling_python_packages = get_sibling_python_packages(projects)
    for name, root in sibling_python_packages.items():
        log.append("Sibling {name} at {root}".format(name=name, root=root))
    for package in get_installed_packages(tox_python):
        log.append(
            "Found {name} python package installed".format(name=package.name))
        if package.name == package_name:
            # We don't need to re-process ourself. We've filtered ourselves
            # from the source dir list, but let's be sure nothing is weird.
            log.append(
                "Skipping {name} because it's us".format(name=package.name))
            continue
        if package.name in sibling_python_packages:
            log.append(
                "Package {name} on system in {root}".format(
                    name=package.name,
                    root=sibling_python_packages[package.name]))
            changed = True

            log.append("Uninstalling {name}".format(name=package.name))
            uninstall_output = subprocess.check_output(
                [tox_python, '-m', 'pip', 'uninstall', '-y', package.name],
                stderr=subprocess.STDOUT)
            log.extend(uninstall_output.decode('utf-8').split('\n'))

            # TODO(mordred) Account for upper-constraints during this install
            log.append(
                "Installing {name} from {root}".format(
                    name=package.name,
                    root=sibling_python_packages[package.name]))
            install_output = subprocess.check_output(
                [tox_python, '-m', 'pip', 'install',
                 '-e', sibling_python_packages[package.name]])
            log.extend(install_output.decode('utf-8').split('\n'))

    log_text = "\n".join(log)
    module.append_to_file(log_file, log_text)
    module.exit_json(changed=changed, msg=log_text)


if __name__ == '__main__':
    main()
