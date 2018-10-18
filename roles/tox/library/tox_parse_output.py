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
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: tox_parse_output
short_description: Parses the output of tox looking for per-line comments
author: Monty Taylor (@mordred)
description:
  - Looks for output from the tox command to find content that could be
    returned as inline comments.
requirements:
  - "python >= 3.5"
options:
  tox_output:
    description:
      - Output from the tox command run
    required: true
    type: str
'''
from ansible.module_utils.basic import AnsibleModule


def extract_file_comments(tox_output):
    ret = {}
    for line in tox_output.split('\n'):
        try:
            if not line:
                continue
            if line[0].isspace():
                continue
            if ': ' not in line:
                continue
            (file_info, message) = line.split(': ', 1)
            (file_path, start_line, start_char) = file_info.split(':')
            if file_path.startswith('./'):
                file_path = file_path[2:]
            ret.setdefault(file_path, [])
            ret[file_path].append(dict(line=int(start_line),
                                       message=message))
        except Exception:
            pass
    return ret


def main():
    module = AnsibleModule(
        argument_spec=dict(
            tox_output=dict(required=True, type='str'),
        )
    )
    tox_output = module.params['tox_output']

    file_comments = extract_file_comments(tox_output)
    module.exit_json(changed=False, file_comments=file_comments)


if __name__ == '__main__':
    main()
