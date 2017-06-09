from docutils.parsers.rst import Directive
from sphinx.domains import Domain, ObjType
import os

import yaml


class Layout(object):
    def __init__(self):
        self.jobs = []


class ZuulJobDirective(Directive):
    has_content = True

    def findZuulYaml(self):
        root = self.state.document.settings.env.relfn2path('.')[1]
        while root:
            for fn in ['zuul.yaml', '.zuul.yaml']:
                path = os.path.join(root, fn)
                if os.path.exists(path):
                    return path
            root = os.path.split(root)[0]
        raise Exception("Unable to find zuul.yaml or .zuul.yaml")

    def parseZuulYaml(self, path):
        with open(path) as f:
            data = yaml.safe_load(f)
        layout = Layout()
        for obj in data:
            if 'job' in obj:
                layout.jobs.append(obj['job'])
        return layout

    def run(self):
        fn = self.findZuulYaml()
        layout = self.parseZuulYaml(fn)
        lines = None
        for job in layout.jobs:
            if job['name'] == self.content[0]:
                lines = job.get('description', '')
        if lines:
            lines = lines.split('\n')

        self.state_machine.insert_input(lines, fn)
        return []


class ZuulDomain(Domain):
    name = 'zuul'
    label = 'Zuul'

    object_types = {
        'job':  ObjType('job'),
    }

    directives = {
        'job': ZuulJobDirective,
    }


def setup(app):
    app.add_domain(ZuulDomain)
