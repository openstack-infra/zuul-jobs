# Copyright (C) 2018 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import os
import testtools
import fixtures
import subprocess
import paramiko
import signal

from .sshagent_remove_keys import Agent, run


class AgentFixture(fixtures.Fixture):

    def _setUp(self):
        self.env = {}
        with open('/dev/null', 'r+') as devnull:
            ssh_agent = subprocess.Popen(['ssh-agent'], close_fds=True,
                                         stdout=subprocess.PIPE,
                                         stderr=devnull,
                                         stdin=devnull)
        (output, _) = ssh_agent.communicate()
        output = output.decode('utf8')
        for line in output.split("\n"):
            if '=' in line:
                line = line.split(";", 1)[0]
                (key, value) = line.split('=')
                self.env[key] = value
                os.environ[key] = value
        self.addCleanup(self.stop)

    def stop(self):
        if 'SSH_AGENT_PID' in self.env:
            os.kill(int(self.env['SSH_AGENT_PID']), signal.SIGTERM)


class TestAgent(testtools.TestCase):
    def test_agent(self):
        """Test the ssh agent library"""
        self.useFixture(AgentFixture())
        tmpdir = fixtures.TempDir()
        self.useFixture(tmpdir)

        k1_path = os.path.join(tmpdir.path, 'key1')
        k1 = paramiko.RSAKey.generate(bits=1024)
        k1.write_private_key_file(k1_path)
        self.assertTrue(os.path.exists(k1_path))
        subprocess.call(['ssh-add', k1_path])

        k2_path = os.path.join(tmpdir.path, 'key2')
        k2 = paramiko.RSAKey.generate(bits=1024)
        k2.write_private_key_file(k2_path)
        self.assertTrue(os.path.exists(k2_path))
        with open(k2_path, 'r') as f:
            k2_private = f.read()
        proc = subprocess.Popen(['ssh-add', '-'],
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        proc.communicate(input=k2_private.encode('utf8'))

        a = Agent()
        l = a.list()
        self.assertEqual(2, len(l))

        run(r'^(?!\(stdin\)).*')

        l = a.list()
        self.assertEqual(1, len(l))
        self.assertTrue(b'stdin' in l[0][1])
