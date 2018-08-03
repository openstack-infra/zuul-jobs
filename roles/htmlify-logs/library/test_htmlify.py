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

import gzip
import os

import testtools
import fixtures

from .htmlify import run

FIXTURE_DIR = os.path.join(os.path.dirname(__file__),
                           'test-fixtures')


class TestHTMLify(testtools.TestCase):

    def _test_file(self, fn):
        in_path = os.path.join(FIXTURE_DIR, 'in', fn)
        ref_path = os.path.join(FIXTURE_DIR, 'reference', fn)
        out_root = self.useFixture(fixtures.TempDir()).path
        out_path = os.path.join(out_root, fn)
        run(in_path, out_path)

        if fn.endswith('gz'):
            out = gzip.open(out_path, 'rb')
        else:
            out = open(out_path, 'rb')

        generated_data = out.read()
        reference_data = open(ref_path, 'rb').read()
        self.assertEqual(reference_data, generated_data)

    def test_htmlify(self):
        self._test_file('job-output.txt')
