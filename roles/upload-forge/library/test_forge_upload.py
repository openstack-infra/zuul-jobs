#!/usr/bin/env python

# Copyright (c) 2019 Binero
# Author: Tobias Urdin <tobias.urdin@binero.se>
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


import testtools
from .forge_upload import _get_url


class TestForgeUpload(testtools.TestCase):
    def test_get_url(self):
        base_url = 'https://forgeapi.puppet.com'
        expected = 'https://forgeapi.puppet.com/test'
        self.assertEqual(_get_url(base_url, '/test'), expected)
        self.assertEqual(_get_url(base_url, 'test'), expected)
