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


def main():
    module = AnsibleModule(
        argument_spec=dict(
            hostvars=dict(required=True, type='dict'),
            hosts=dict(required=False, type='list'),
        )
    )

    hostvars = module.params['hostvars']
    hosts = module.params['hosts']
    if not hosts:
        hosts = hostvars.keys()

    known_hosts = set()

    for host in hosts:
        this = hostvars[host]

        public_keys = [x for x in this.keys() if
                       x.startswith('ansible_ssh_host_key')]

        addresses = [this['ansible_host']]
        nodepool = this.get('nodepool', {})
        for nodepool_address in (
                'interface_ip', 'public_ipv4', 'private_ipv4', 'public_ipv6'):
            address = nodepool.get(nodepool_address)
            if address:
                addresses.append(address)

        for iface in this.get('ansible_interfaces', []):
            iface_key = 'ansible_{}'.format(iface.replace('-', '_'))
            ipv4 = this[iface_key].get('ipv4')
            if not isinstance(ipv4, list):
                ipv4 = [ipv4]
            ipv6 = this[iface_key].get('ipv6')
            if not isinstance(ipv6, list):
                ipv6 = [ipv6]
            addresses += [x['address'] for x in ipv4 if x and not
                          x['address'].startswith('127.')]
            addresses += [y['address'] for y in ipv6 if y and not
                          y['scope'] == 'host']
            addresses += [this['ansible_hostname']]

        for addr in set(addresses):
            for key in public_keys:
                if key.endswith('rsa_public'):
                    key_type = 'ssh-rsa'
                elif key.endswith('ecdsa_public'):
                    # XXX This will not work with > 256 bit ecdsa keys
                    # until https://github.com/ansible/ansible/issues/28325
                    # is fixed. We're using the proposed scheme in case it
                    # does merge as-is, but it may need to be updated if
                    # the patch is changed as well.
                    key_type = this.get('{}_type'.format(key),
                                        'ecdsa-sha2-nistp256')
                elif key.endswith('ed25519_public'):
                    key_type = 'ssh-ed25519'
                else:
                    continue
                known_hosts.add(
                    '{addr} {key_type} {key}'.format(addr=addr,
                                                     key_type=key_type,
                                                     key=this[key]))

    ret = {
        'ansible_facts': {
            'all_known_hosts': [dict(name=x.split()[0], key=x) for x in
                                sorted(known_hosts)]
        }
    }

    module.exit_json(changed=False, _zuul_nolog_return=True, **ret)

from ansible.module_utils.basic import *  # noqa
from ansible.module_utils.basic import AnsibleModule

if __name__ == '__main__':
    main()
