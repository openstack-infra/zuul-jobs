#!/usr/bin/python

# Copyright (c) 2018 Red Hat
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
import traceback


command_map = {
    'network_interfaces': 'ip address show',
    'network_routing_v4': 'ip route show',
    'network_routing_v6': 'ip -6 route show',
    'network_neighbors': 'ip neighbor show',
}


def run_command(command):
    env = os.environ.copy()
    env['PATH'] = '{path}:/sbin:/usr/sbin'.format(path=env['PATH'])
    return subprocess.check_output(
        shlex.split(command),
        stderr=subprocess.STDOUT,
        env=env)


def collect_unbound_logs():
    '''Look for unbound logs

    This looks for unbound logs in common places and returns the
    contents.  Intended for the failure path to add more info if the
    traceroutes have failed.
    '''
    ret = {}

    # NOTE(ianw): keep this one first, the other exists but isn't
    # populated on infra rpm images for ... reasons
    if os.path.exists('/var/lib/unbound/unbound.log'):
        unbound_log_file = '/var/lib/unbound/unbound.log'
    elif os.path.exists('/var/log/unbound.log'):
        unbound_log_file = '/var/log/unbound.log'
    else:
        return ret

    with open(unbound_log_file) as f:
        ret['unbound_log_file'] = unbound_log_file
        # NOTE(ianw): At high verbosity this can be big ... but this
        # is also intended to be used early which should limit it's
        # size.  We could tail it ...
        ret['unbound_log_file_content'] = f.read()

    return ret


def main():
    module = AnsibleModule(
        argument_spec=dict(
            traceroute_host=dict(required=True, type='str'),
        )
    )

    traceroute_host = module.params['traceroute_host']

    ret = {}

    for key, command in command_map.items():
        try:
            ret[key] = run_command(command)
        except subprocess.CalledProcessError:
            pass

    passed = False
    try:
        ret['traceroute_v6'] = run_command(
            'traceroute6 -n {host}'.format(host=traceroute_host))
        passed = True
    except (subprocess.CalledProcessError, OSError) as e:
        ret['traceroute_v6_exception'] = traceback.format_exc(e)
        ret['traceroute_v6_output'] = e.output
        ret['traceroute_v6_return'] = e.returncode
        pass
    try:
        ret['traceroute_v4'] = run_command(
            'traceroute -n {host}'.format(host=traceroute_host))
        passed = True
    except (subprocess.CalledProcessError, OSError) as e:
        ret['traceroute_v4_exception'] = traceback.format_exc(e)
        ret['traceroute_v4_output'] = e.output
        ret['traceroute_v4_return'] = e.returncode
        pass
    if not passed:
        ret.update(collect_unbound_logs())
        module.fail_json(
            msg="No viable v4 or v6 route found to {traceroute_host}."
            " The build node is assumed to be invalid.".format(
                traceroute_host=traceroute_host), **ret)

    module.exit_json(changed=False, _zuul_nolog_return=True, **ret)

from ansible.module_utils.basic import *  # noqa
from ansible.module_utils.basic import AnsibleModule

if __name__ == '__main__':
    main()
