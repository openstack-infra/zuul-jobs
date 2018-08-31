# Copyright 2018 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import argparse
import os
import socket
import struct
import sys
import re

from ansible.module_utils.basic import AnsibleModule


SSH_AGENT_FAILURE = 5
SSH_AGENT_SUCCESS = 6
SSH_AGENT_IDENTITIES_ANSWER = 12

SSH_AGENTC_REQUEST_IDENTITIES = 11
SSH_AGENTC_REMOVE_IDENTITY = 18


def unpack_string(data):
    (l,) = struct.unpack('!i', data[:4])
    d = data[4:4 + l]
    return (d, data[4 + l:])


def pack_string(data):
    ret = struct.pack('!i', len(data))
    return ret + data


class Agent(object):
    def __init__(self):
        path = os.environ['SSH_AUTH_SOCK']
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(path)

    def send(self, message_type, contents):
        payload = struct.pack('!ib', len(contents) + 1, message_type)
        payload += bytearray(contents)
        self.sock.send(payload)

    def recv(self):
        buf = b''
        while len(buf) < 5:
            buf += self.sock.recv(1)
        message_len, message_type = struct.unpack('!ib', buf[:5])
        buf = buf[5:]
        while len(buf) < message_len - 1:
            buf += self.sock.recv(1)
        return message_type, buf

    def list(self):
        self.send(SSH_AGENTC_REQUEST_IDENTITIES, b'')
        mtype, data = self.recv()
        if mtype != SSH_AGENT_IDENTITIES_ANSWER:
            raise Exception("Invalid response to list")
        (nkeys,) = struct.unpack('!i', data[:4])
        data = data[4:]
        keys = []
        for i in range(nkeys):
            blob, data = unpack_string(data)
            comment, data = unpack_string(data)
            keys.append((blob, comment))
        return keys

    def remove(self, blob):
        self.send(SSH_AGENTC_REMOVE_IDENTITY, pack_string(blob))
        mtype, data = self.recv()
        if mtype != SSH_AGENT_SUCCESS:
            raise Exception("Key was not removed")


def run(remove):
    a = Agent()
    keys = a.list()
    removed = []
    to_remove = re.compile(remove)
    for blob, comment in keys:
        if not to_remove.match(comment.decode('utf8')):
            continue
        a.remove(blob)
        removed.append(comment)
    return removed


def ansible_main():
    module = AnsibleModule(
        argument_spec=dict(
            remove=dict(required=True, type='str')))

    removed = run(module.params.get('remove'))

    module.exit_json(changed=(removed != []),
                     removed=removed)


def cli_main():
    parser = argparse.ArgumentParser(
        description="Remove ssh keys from agent"
    )
    parser.add_argument('remove', nargs='+',
                        help='regex matching comments of keys to remove')
    args = parser.parse_args()

    removed = run(args.remove)
    print(removed)


if __name__ == '__main__':
    if sys.stdin.isatty():
        cli_main()
    else:
        ansible_main()
