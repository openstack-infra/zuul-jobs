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
    'network_interfaces': 'ip address show',
    'network_routing_v4': 'ip route show',
    'network_routing_v6': 'ip -6 route show',
    'network_neighbors': 'ip neighbor show',
}


def run_command(command):
    env = os.environ.copy()
    env['PATH'] = '{path}:/sbin'.format(path=env['PATH'])
    return subprocess.check_output(
        shlex.split(command),
        stderr=subprocess.STDOUT,
        env=env)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            image_manifest=dict(required=False, type='str'),
            traceroute_host=dict(required=False, type='str'),
        )
    )

    image_manifest = module.params['image_manifest']
    traceroute_host = module.params['traceroute_host']
    ret = {'image_manifest': None, 'traceroute': None}

    if image_manifest and os.path.exists(image_manifest):
        ret['image_manifest'] = open(image_manifest, 'r').read()
    if traceroute_host:
        passed = False
        try:
            ret['traceroute_v6'] = run_command(
                'traceroute6 -n {host}'.format(host=traceroute_host))
            passed = True
        except subprocess.CalledProcessError:
            pass
        try:
            ret['traceroute_v4'] = run_command(
                'traceroute -n {host}'.format(host=traceroute_host))
            passed = True
        except subprocess.CalledProcessError:
            pass
        if not passed:
            module.fail_json(
                msg="No viable v4 or v6 route found to {traceroute_host}."
                    " The build node is assumed to be invalid.".format(
                        traceroute_host=traceroute_host))

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
