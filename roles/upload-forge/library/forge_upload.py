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


ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}


DOCUMENTATION = '''
---
module: forge_upload

short_description: Uploads a puppet module tarball to a Forge server.

description:
    - "Uploads a puppet module tarball to a Forge server."

options:
    username:
        description:
            - The username to the Forge account
        required: true
    password:
        description:
            - The password to the Forge account
        required: true
    tarball:
        description:
            - The absolute path to the tarball of the puppet module
              that should be uploaded
        required: true
    forgeapi:
        description:
            - This base url to the Forge server API, defaults to
              https://forgeapi.puppet.com
        required: false

author:
    - Tobias Urdin (@tobias-urdin)
'''


EXAMPLES = '''
- name: Upload module
  forge_upload:
    username: 'myuser'
    password: 'mypass'
    tarball: '/home/myuser/test/pkg/myuser-test-0.1.0.tar.gz'
'''


RETURN = '''
msg:
    description: The output message from the module.
'''


from ansible.module_utils.basic import AnsibleModule  # noqa
import os  # noqa
import requests  # noqa


# Client ID and secret from puppet-blacksmith
CLIENT_ID = 'b93eb708fd942cfc7b4ed71db6ce219b814954619dbe537ddfd208584e8cff8d'
CLIENT_SECRET = '216648059ad4afec3e4d77bd9e67817c095b2dcf94cdec18ac3d00584f863180'  # noqa

FORGEAPI = 'https://forgeapi.puppet.com'


def _get_url(forgeapi, path):
    path = path[1:] if path.startswith('/') else path
    return '%s/%s' % (forgeapi, path)


def _forge_auth(forgeapi, username, password):
    url = _get_url(forgeapi, '/oauth/token')
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'username': username,
        'password': password,
        'grant_type': 'password',
    }
    headers = {
        'User-Agent': 'forge_upload-ansible-module/1.0',
    }
    response = requests.post(url, json=data, headers=headers)
    return response


def _forge_upload(forgeapi, token, tarball):
    url = _get_url(forgeapi, '/v2/releases')
    data = {
        'file': open(tarball, 'rb').read(),
    }
    headers = {
        'User-Agent': 'forge_upload-ansible-module/1.0',
        'Authorization': 'Bearer %s' % token,
    }
    response = requests.post(url, files=data, headers=headers)
    return response


def run_module():
    module_args = dict(
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        tarball=dict(type='str', required=True),
        forgeapi=dict(type='str', default=FORGEAPI),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    tarball = module.params['tarball']
    if os.path.exists(tarball) is False:
        module.fail_json(msg='Tarball %s does not exist' % tarball, **result)

    resp = _forge_auth(module.params['forgeapi'],
                       module.params['username'],
                       module.params['password'])

    if resp.status_code != 200:
        msg = 'Forge API auth failed with code: %d' % resp.status_code
        module.fail_json(msg=msg, **result)

    if module.check_mode:
        return result

    auth = resp.json()
    token = auth['access_token']

    resp = _forge_upload(module.params['forgeapi'], token, tarball)

    if resp.status_code == 409:
        msg = 'Module %s already exists on Forge' % tarball
        module.exit_json(msg=msg, **result)

    if resp.status_code != 201:
        try:
            data = resp.json()
            errors = ','.join(data['errors'])
        except Exception:
            errors = 'unknown'
        msg = 'Forge API failed to upload tarball with code: %d errors: %s' % (
            resp.status_code, errors)
        module.fail_json(msg=msg, **result)

    result['changed'] = True
    module.exit_json(msg='Successfully uploaded tarball %s' % tarball,
                     **result)


def main():
    run_module()


if __name__ == '__main__':
    main()
