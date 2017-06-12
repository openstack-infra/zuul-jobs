# Copyright 2017 Red Hat, Inc.
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

from sphinx import addnodes
from docutils.parsers.rst import Directive
from sphinx.domains import Domain, ObjType
from sphinx.directives import ObjectDescription
import os

import yaml


class Layout(object):
    def __init__(self):
        self.jobs = []


class BaseZuulDirective(Directive):
    has_content = True

    def find_zuul_yaml(self):
        root = self.state.document.settings.env.relfn2path('.')[1]
        while root:
            for fn in ['zuul.yaml', '.zuul.yaml']:
                path = os.path.join(root, fn)
                if os.path.exists(path):
                    return path
            root = os.path.split(root)[0]
        raise Exception("Unable to find zuul.yaml or .zuul.yaml")

    def parse_zuul_yaml(self, path):
        with open(path) as f:
            data = yaml.safe_load(f)
        layout = Layout()
        for obj in data:
            if 'job' in obj:
                layout.jobs.append(obj['job'])
        return layout

    def _parse_zuul_layout(self):
        env = self.state.document.settings.env
        if not env.domaindata['zuul']['layout']:
            path = self.find_zuul_yaml()
            layout = self.parse_zuul_yaml(path)
            env.domaindata['zuul']['layout_path'] = path
            env.domaindata['zuul']['layout'] = layout

    @property
    def zuul_layout(self):
        self._parse_zuul_layout()
        env = self.state.document.settings.env
        return env.domaindata['zuul']['layout']

    @property
    def zuul_layout_path(self):
        self._parse_zuul_layout()
        env = self.state.document.settings.env
        return env.domaindata['zuul']['layout_path']

    def generate_zuul_job_content(self, name):
        lines = []
        for job in self.zuul_layout.jobs:
            if job['name'] == name:
                lines.append('.. zuul:job:: %s' % name)
                if 'branches' in job:
                    branches = job['branches']
                    if not isinstance(branches, list):
                        branches = [branches]
                    variant = ', '.join(branches)
                    lines.append('   :variant: %s' % variant)
                lines.append('')
                for l in job.get('description', '').split('\n'):
                    lines.append('   ' + l)
                lines.append('')
        return lines

    def find_zuul_roles(self):
        root = os.path.dirname(self.zuul_layout_path)
        roledir = os.path.join(root, 'roles')
        env = self.state.document.settings.env
        roles = env.domaindata['zuul']['role_paths']
        for p in os.listdir(roledir):
            role_readme = os.path.join(roledir, p, 'README.rst')
            if os.path.exists(role_readme):
                roles[p] = role_readme

    @property
    def zuul_role_paths(self):
        env = self.state.document.settings.env
        roles = env.domaindata['zuul']['role_paths']
        if roles is None:
            roles = {}
            env.domaindata['zuul']['role_paths'] = roles
            self.find_zuul_roles()
        return roles

    def generate_zuul_role_content(self, name):
        lines = []
        lines.append('.. zuul:role:: %s' % name)
        lines.append('')
        role_readme = self.zuul_role_paths[name]
        with open(role_readme) as f:
            role_lines = f.read().split('\n')
            for l in role_lines:
                lines.append('   ' + l)
        return lines


class ZuulJobDirective(BaseZuulDirective, ObjectDescription):
    option_spec = {
        'variant': lambda x: x,
    }

    def handle_signature(self, sig, signode):
        signode += addnodes.desc_name(sig, sig)
        return sig

    def add_target_and_index(self, name, sig, signode):
        targetname = self.objtype + '-' + name
        if 'variant' in self.options:
            targetname += '-' + self.options['variant']
        if targetname not in self.state.document.ids:
            signode['names'].append(targetname)
            signode['ids'].append(targetname)
            signode['first'] = (not self.names)
            self.state.document.note_explicit_target(signode)

        indextext = '%s (%s)' % (name, self.objtype)
        self.indexnode['entries'].append(('single', indextext,
                                          targetname, '', None))


class ZuulAutoJobDirective(BaseZuulDirective):
    def run(self):
        name = self.content[0]
        lines = self.generate_zuul_job_content(name)
        self.state_machine.insert_input(lines, self.zuul_layout_path)
        return []


class ZuulAutoJobsDirective(BaseZuulDirective):
    has_content = False

    def run(self):
        lines = []
        names = set()
        for job in self.zuul_layout.jobs:
            name = job['name']
            if name in names:
                continue
            lines.extend(self.generate_zuul_job_content(name))
            names.add(name)
        self.state_machine.insert_input(lines, self.zuul_layout_path)
        return []


class ZuulRoleDirective(BaseZuulDirective, ObjectDescription):
    def handle_signature(self, sig, signode):
        signode += addnodes.desc_name(sig, sig)
        return sig

    def add_target_and_index(self, name, sig, signode):
        targetname = self.objtype + '-' + name
        if targetname not in self.state.document.ids:
            signode['names'].append(targetname)
            signode['ids'].append(targetname)
            signode['first'] = (not self.names)
            self.state.document.note_explicit_target(signode)

        indextext = '%s (%s)' % (name, self.objtype)
        self.indexnode['entries'].append(('single', indextext,
                                          targetname, '', None))


class ZuulAutoRoleDirective(BaseZuulDirective):
    def run(self):
        name = self.content[0]
        lines = self.generate_zuul_role_content(name)
        self.state_machine.insert_input(lines, self.zuul_role_paths[name])
        return []


class ZuulAutoRolesDirective(BaseZuulDirective):
    has_content = False

    def run(self):
        role_names = reversed(sorted(self.zuul_role_paths.keys()))
        for name in role_names:
            lines = self.generate_zuul_role_content(name)
            self.state_machine.insert_input(lines, self.zuul_role_paths[name])
        return []


class ZuulDomain(Domain):
    name = 'zuul'
    label = 'Zuul'

    object_types = {
        'job': ObjType('job'),
        'role': ObjType('role'),
    }

    directives = {
        'job': ZuulJobDirective,
        'autojob': ZuulAutoJobDirective,
        'autojobs': ZuulAutoJobsDirective,
        'role': ZuulRoleDirective,
        'autorole': ZuulAutoRoleDirective,
        'autoroles': ZuulAutoRolesDirective,
    }

    initial_data = {
        'layout': None,
        'layout_path': None,
        'role_paths': None,
    }


def setup(app):
    app.add_domain(ZuulDomain)
