#!/bin/bash

# Copyright (c) 2018 Red Hat, Inc.
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
# See the License for the specific language governing permissions and
# limitations under the License.

set -eu

zuul_work_dir=$1
# Use cd in the script rather than chdir from the script module. The chdir
# has some source-code comments that indicate for script that it needs to be
# an absolute path. Since our zuul_work_dir defaults to
# "src/{{ zuul.project.src_dir }}" in many places, that could be rather bad.
# The script can ensure it starts from the home dir and then change into the
# directory, which should work for both relative and absolute paths.
cd $HOME
cd $zuul_work_dir

# Add all the tox envs to the path so that type will work. Prefer tox
# envs to system path. If there is more than one tox env, it doesn't
# matter which one we use, PATH will find the first command.
if [[ -d .tox ]] ; then
    for tox_bindir in $(find .tox -mindepth 2 -maxdepth 2 -name 'bin') ; do
        PATH=$(pwd)/$tox_bindir:$PATH
    done
fi

# NOTE(mordred): Fallback default to /usr/os-testr-env/bin/subunit2html
# to provide a fallback case for OpenStack while we make sure this
# logic works. Once we're satisfied that nobody is using
# /usr/os-testr-env/bin/subunit2html, we can remove this.
PATH="$PATH:/usr/os-testr-env/bin"

type -p subunit2html
