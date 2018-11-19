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

import os
import shlex
import subprocess


command_map = {
    'uname': 'uname -a',
}


def run_command(command):
    env = os.environ.copy()
    env['PATH'] = '{path}:/sbin:/usr/sbin'.format(path=env['PATH'])
    return subprocess.check_output(
        shlex.split(command),
        stderr=subprocess.STDOUT,
        env=env)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            image_manifest=dict(required=False, type='str'),
            image_manifest_files=dict(required=False, type='list'),
        )
    )

    image_manifest = module.params['image_manifest']
    image_manifest_files = module.params['image_manifest_files']
    if not image_manifest_files and image_manifest:
        image_manifest_files = [image_manifest]
    ret = {'image_manifest_files': []}

    for image_manifest in image_manifest_files:
        if image_manifest and os.path.exists(image_manifest):
            ret['image_manifest_files'].append({
                'filename': image_manifest,
                # Do this in python cause it's easier than in jinja2
                'underline': len(image_manifest) * '-',
                'content': open(image_manifest, 'r').read(),
            })

    for key, command in command_map.items():
        try:
            ret[key] = run_command(command)
        except subprocess.CalledProcessError:
            pass

    module.exit_json(changed=False, _zuul_nolog_return=True, **ret)

from ansible.module_utils.basic import *  # noqa
from ansible.module_utils.basic import AnsibleModule

if __name__ == '__main__':
    main()
