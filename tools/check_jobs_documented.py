#!/usr/bin/env python
#
# Copyright 2019 Red Hat, Inc.
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

# Ensure that all jobs and roles appear in the documentation.

import os
import re
import sys
import yaml


class ZuulSafeLoader(yaml.SafeLoader):

    def __init__(self, *args, **kwargs):
        super(ZuulSafeLoader, self).__init__(*args, **kwargs)
        self.add_multi_constructor('!encrypted/', self.construct_encrypted)

    @classmethod
    def construct_encrypted(cls, loader, tag_suffix, node):
        return loader.construct_sequence(node)


class Layout(object):
    def __init__(self):
        self.jobs = []


class ZuulConfig(object):
    def find_zuul_yaml(self):
        root = os.getcwd()
        while root:
            for fn in ['zuul.yaml', '.zuul.yaml', 'zuul.d', '.zuul.d']:
                path = os.path.join(root, fn)
                if os.path.exists(path):
                    return path
            root = os.path.split(root)[0]
        raise Exception(
            "Unable to find zuul config in zuul.yaml, .zuul.yaml,"
            " zuul.d or .zuul.d")

    def parse_zuul_yaml(self, path):
        with open(path) as f:
            data = yaml.load(f, Loader=ZuulSafeLoader)
        layout = Layout()
        for obj in data:
            if 'job' in obj:
                layout.jobs.append(obj['job'])
        return layout

    def parse_zuul_d(self, path):
        layout = Layout()
        for conf in os.listdir(path):
            with open(os.path.join(path, conf)) as f:
                data = yaml.load(f, Loader=ZuulSafeLoader)
            for obj in data:
                if 'job' in obj:
                    layout.jobs.append(obj['job'])
        return layout

    def parse_zuul_layout(self):
        path = self.find_zuul_yaml()
        if path.endswith('zuul.d'):
            layout = self.parse_zuul_d(path)
        else:
            layout = self.parse_zuul_yaml(path)
        return layout

    def __init__(self):
        self.layout = self.parse_zuul_layout()


class Docs(object):
    def __init__(self):
        self.jobs = set()
        self.roles = set()
        self.autojobs = False
        self.autoroles = False
        self.walk(os.path.join(os.getcwd(), 'doc', 'source'))

    def walk(self, path):
        for root, dirs, files in os.walk(path):
            for fn in files:
                if fn.endswith('.rst'):
                    with open(os.path.join(root, fn)) as f:
                        for line in f:
                            m = re.match(r'.*\.\. zuul:job:: (.*)$', line)
                            if m:
                                self.jobs.add(m.group(1))
                            m = re.match(r'.*\.\. zuul:autojob:: (.*)$', line)
                            if m:
                                self.jobs.add(m.group(1))
                            m = re.match(r'.*\.\. zuul:autojobs::.*$', line)
                            if m:
                                self.autojobs = True
                            m = re.match(r'.*\.\. zuul:role:: (.*)$', line)
                            if m:
                                self.roles.add(m.group(1))
                            m = re.match(r'.*\.\. zuul:autorole:: (.*)$', line)
                            if m:
                                self.roles.add(m.group(1))
                            m = re.match(r'.*\.\. zuul:autoroles::.*$', line)
                            if m:
                                self.autoroles = True


class Roles(object):
    def __init__(self):
        self.roles = set()
        self.walk(os.path.join(os.getcwd(), 'roles'))

    def walk(self, path):
        for role in os.listdir(path):
            if os.path.isdir(os.path.join(path, role, 'tasks')):
                self.roles.add(role)


z = ZuulConfig()
r = Roles()
d = Docs()

ret = 0
for role in r.roles:
    if role not in d.roles:
        print("Role %s not included in document tree" % (role,))
        ret = 1
for job in [x['name'] for x in z.layout.jobs]:
    if job not in d.jobs:
        print("Job %s not included in document tree" % (job,))
        ret = 1

sys.exit(ret)
