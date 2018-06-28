# Copyright 2013 IBM Corp.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import unittest


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    base_path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
    # Load role tests
    for role_dir in os.listdir('roles'):
        full_role_dir = os.path.join(base_path, 'roles', role_dir)
        lib_dir = os.path.join(full_role_dir, 'library')
        if not os.path.exists(lib_dir):
            continue
        if not pattern:
            suite.addTests(loader.discover(lib_dir,
                                           top_level_dir=base_path))
        else:
            suite.addTests(loader.discover(lib_dir, pattern=pattern,
                           top_level_dir=base_path))

    return suite
