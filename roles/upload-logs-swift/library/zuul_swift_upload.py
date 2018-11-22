#!/usr/bin/env python3
#
# Copyright 2014 Rackspace Australia
# Copyright 2018 Red Hat, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


"""
Utility to upload files to swift
"""

import argparse
import logging
import mimetypes
import os
try:
    import queue as queuelib
except ImportError:
    import Queue as queuelib
import stat
import sys
import tempfile
import threading
import time
import zlib
import collections

import openstack
import requests
import requests.exceptions
import requestsexceptions

from ansible.module_utils.basic import AnsibleModule

try:
    # Python 3.3+
    from collections.abc import Sequence
except ImportError:
    from collections import Sequence

mimetypes.init()
mimetypes.add_type('text/plain', '.yaml')

MAX_UPLOAD_THREADS = 24
POST_ATTEMPTS = 3

# Map mime types to apache icons
APACHE_MIME_ICON_MAP = {
    '_default': 'unknown.png',
    'application/gzip': 'compressed.png',
    'application/directory': 'folder.png',
    'text/html': 'text.png',
    'text/plain': 'text.png',
}

# Map mime types to apache icons
APACHE_FILE_ICON_MAP = {
    '..': 'back.png',
}

# These icon files are from the Apache project and are in the public
# domain.
ICON_IMAGES = {
    'back.png': 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAWCAMAAAD3n0w0AAAAElBMVEX/'
                '///M//+ZmZlmZmYzMzMAAACei5rnAAAAAnRSTlP/AOW3MEoAAABWSURB'
                'VHjabdBBCgAhDEPRRpv7X3kwEMsQ//IRRC08urjRHbha5VLFUsVSxVI9'
                'lmDh5hMpHD6n0EgoiZG0DNINpnWlcVXaRix76e1/8dddcL6nG0Ri9gHj'
                'tgSXKYeLBgAAAABJRU5ErkJggg==',
    'compressed.png': 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAWCAMAAAD3n0w0AAADAFBM'
                      'VEX//////8z//5n//2b//zP//wD/zP//zMz/zJn/zGb/zDP/zAD/'
                      'mf//mcz/mZn/mWb/mTP/mQD/Zv//Zsz/Zpn/Zmb/ZjP/ZgD/M///'
                      'M8z/M5n/M2b/MzP/MwD/AP//AMz/AJn/AGb/ADP/AADM///M/8zM'
                      '/5nM/2bM/zPM/wDMzP/MzMzMzJnMzGbMzDPMzADMmf/MmczMmZnM'
                      'mWbMmTPMmQDMZv/MZszMZpnMZmbMZjPMZgDMM//MM8zMM5nMM2bM'
                      'MzPMMwDMAP/MAMzMAJnMAGbMADPMAACZ//+Z/8yZ/5mZ/2aZ/zOZ'
                      '/wCZzP+ZzMyZzJmZzGaZzDOZzACZmf+ZmcyZmZmZmWaZmTOZmQCZ'
                      'Zv+ZZsyZZpmZZmaZZjOZZgCZM/+ZM8yZM5mZM2aZMzOZMwCZAP+Z'
                      'AMyZAJmZAGaZADOZAABm//9m/8xm/5lm/2Zm/zNm/wBmzP9mzMxm'
                      'zJlmzGZmzDNmzABmmf9mmcxmmZlmmWZmmTNmmQBmZv9mZsxmZplm'
                      'ZmZmZjNmZgBmM/9mM8xmM5lmM2ZmMzNmMwBmAP9mAMxmAJlmAGZm'
                      'ADNmAAAz//8z/8wz/5kz/2Yz/zMz/wAzzP8zzMwzzJkzzGYzzDMz'
                      'zAAzmf8zmcwzmZkzmWYzmTMzmQAzZv8zZswzZpkzZmYzZjMzZgAz'
                      'M/8zM8wzM5kzM2YzMzMzMwAzAP8zAMwzAJkzAGYzADMzAAAA//8A'
                      '/8wA/5kA/2YA/zMA/wAAzP8AzMwAzJkAzGYAzDMAzAAAmf8AmcwA'
                      'mZkAmWYAmTMAmQAAZv8AZswAZpkAZmYAZjMAZgAAM/8AM8wAM5kA'
                      'M2YAMzMAMwAAAP8AAMwAAJkAAGYAADPuAADdAAC7AACqAACIAAB3'
                      'AABVAABEAAAiAAARAAAA7gAA3QAAuwAAqgAAiAAAdwAAVQAARAAA'
                      'IgAAEQAAAO4AAN0AALsAAKoAAIgAAHcAAFUAAEQAACIAABHu7u7d'
                      '3d27u7uqqqqIiIh3d3dVVVVEREQiIiIREREAAAD7CIKZAAAAJXRS'
                      'TlP///////////////////////////////////////////////8A'
                      'P89CTwAAAGtJREFUeNp9z9ENgDAIhOEOco+dybVuEXasFMRDY/x5'
                      '+xJCO6Znu6kSx7BhXyjtKBWWNlwW88Loid7hFRKBXiIYCMfMEYUQ'
                      'QohC3CjFA5nIjqx1CqlDLGR/EhM5O06yvin0ftGOyIS7lV14AsQN'
                      'aR7rMEBYAAAAAElFTkSuQmCC',
    'folder.png': 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAWCAMAAAD3n0w0AAAAElBMVEX/'
                  '////zJnM//+ZZjMzMzMAAADCEvqoAAAAA3RSTlP//wDXyg1BAAAASElE'
                  'QVR42s3KQQ6AQAhDUaXt/a/sQDrRJu7c+NmQB0e99B3lnqjT6cYx6zSI'
                  'bV40n3D7psYMoBoz4w8/EdNYQsbGEjNxYSljXTEsA9O1pLTvAAAAAElF'
                  'TkSuQmCC',
    'text.png': 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAWCAMAAAD3n0w0AAAAD1BMVEX/'
                '///M//+ZmZkzMzMAAABVsTOVAAAAAnRSTlP/AOW3MEoAAABISURBVHja'
                'tcrRCgAgCENRbf7/N7dKomGvngjhMsPLD4NdMPwia438NRIyxsaL/XQZ'
                'hyxpkC6zyjLXGVXnkhqWJWIIrOgeinECLlUCjBCqNQoAAAAASUVORK5C'
                'YII=',
    'unknown.png': 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAWCAMAAAD3n0w0AAAAD1BMVEX/'
                   '///M//+ZmZkzMzMAAABVsTOVAAAAAnRSTlP/AOW3MEoAAABYSURBVHja'
                   'ncvRDoAgDEPRruX/v1kmNHPBxMTLyzgD6FmsILg56g2hQnJkOco4yZhq'
                   'tN5nYd5Zq0LsHblwxwP9GTCWsaGtoelANKzOlz/RfaLYUmLE6E28ALlN'
                   'AupSdoFsAAAAAElFTkSuQmCC'}


def get_mime_icon(mime, filename=''):
    icon = (APACHE_FILE_ICON_MAP.get(filename) or
            APACHE_MIME_ICON_MAP.get(mime) or
            APACHE_MIME_ICON_MAP['_default'])
    return "data:image/png;base64,%s" % ICON_IMAGES[icon]


def sizeof_fmt(num, suffix='B'):
    # From http://stackoverflow.com/questions/1094841/
    # reusable-library-to-get-human-readable-version-of-file-size
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)


class FileDetail():
    """
    Used to generate indexes with links or as the file path
    to push to swift.
    """

    def __init__(self, full_path, relative_path, filename=None):
        """
        Args:
            full_path (str): The absolute path to the file on disk.
            relative_path (str): The relative path from the artifacts source
                                 used for links.
            filename (str): An optional alternate filename in links.
        """
        self.full_path = full_path
        if filename is None:
            self.filename = os.path.basename(full_path)
        else:
            self.filename = filename
        self.relative_path = relative_path

        if self.full_path and os.path.isfile(self.full_path):
            mime_guess, encoding = mimetypes.guess_type(self.full_path)
            self.mimetype = mime_guess if mime_guess else 'text/plain'
            self.encoding = encoding
            self.folder = False
        else:
            self.mimetype = 'application/directory'
            self.encoding = None
            self.folder = True
        if self.full_path:
            st = os.stat(self.full_path)
            self.last_modified = time.gmtime(st[stat.ST_MTIME])
            self.size = st[stat.ST_SIZE]
        else:
            self.last_modified = time.gmtime(0)
            self.size = 0

    def __repr__(self):
        t = 'Folder' if self.folder else 'File'
        return '<%s %s>' % (t, self.relative_path)


class FileList(Sequence):
    '''A collection of FileDetail objects

    This is a list-like group of FileDetail objects, intended to be
    used as a context manager around the upload process.
    '''
    def __init__(self):
        self.file_list = []
        self.file_list.append(FileDetail(None, '', ''))

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __getitem__(self, item):
        return self.file_list.__getitem__(item)

    def __len__(self):
        return self.file_list.__len__()

    @staticmethod
    def _path_in_tree(root, path):
        full_path = os.path.realpath(os.path.abspath(
            os.path.expanduser(path)))
        if not full_path.startswith(root):
            logging.debug("Skipping path outside root: %s" % (path,))
            return False
        return True

    def add(self, file_path):
        """
        Generate a list of files to upload to swift. Recurses through
        directories
        """

        # file_list: A list of FileDetails to push to swift
        file_list = []

        if os.path.isfile(file_path):
            relative_path = os.path.basename(file_path)
            file_list.append(FileDetail(file_path, relative_path))
        elif os.path.isdir(file_path):
            original_root = os.path.realpath(os.path.abspath(
                os.path.expanduser(file_path)))

            parent_dir = os.path.dirname(file_path)
            if not file_path.endswith('/'):
                filename = os.path.basename(file_path)
                full_path = file_path
                relative_name = os.path.relpath(full_path, parent_dir)
                file_list.append(FileDetail(full_path, relative_name,
                                            filename))
            # TODO: this will copy the result of symlinked files, but
            # it won't follow directory symlinks.  If we add that, we
            # should ensure that we don't loop.
            for path, folders, files in os.walk(file_path):
                # Sort folder in-place so that we recurse in order.
                files.sort(key=lambda x: x.lower())
                folders.sort(key=lambda x: x.lower())
                # relative_path: The path between the given directory
                # and the one being currently walked.
                relative_path = os.path.relpath(path, parent_dir)

                for filename in folders:
                    full_path = os.path.join(path, filename)
                    if not self._path_in_tree(original_root, full_path):
                        continue
                    relative_name = os.path.relpath(full_path, parent_dir)
                    file_list.append(FileDetail(full_path, relative_name,
                                                filename))

                for filename in files:
                    full_path = os.path.join(path, filename)
                    if not self._path_in_tree(original_root, full_path):
                        continue
                    relative_name = os.path.relpath(full_path, parent_dir)
                    file_detail = FileDetail(full_path, relative_name)
                    file_list.append(file_detail)

        self.file_list += file_list


class Indexer():
    """generates index.html files if requested."""

    def __init__(self, create_parent_links=True,
                 create_topdir_parent_link=False,
                 append_footer='index_footer.html'):
        self.create_parent_links = create_parent_links
        self.create_topdir_parent_link = create_topdir_parent_link
        self.append_footer = append_footer
        self.index_filename = 'index.html'

    def make_indexes(self, file_list):
        '''Make index files

        Args:
            file_list (FileList): A FileList object to be updated
             with index files for each directory.
        Return:
            No value, the file_list will be updated
        '''
        assert isinstance(file_list, FileList)

        folders = collections.OrderedDict()
        for f in file_list:
            if f.folder:
                folders[f.relative_path] = []
                folder = os.path.dirname(os.path.dirname(
                    f.relative_path + '/'))
                if folder == '/':
                    folder = ''
            else:
                folder = os.path.dirname(f.relative_path)
            folders[folder].append(f)

        indexes = {}
        parent_file_detail = FileDetail(None, '..', '..')
        for folder, files in folders.items():
            # Don't add the pseudo-top-directory
            if files and files[0].full_path is None:
                files = files[1:]
                if self.create_topdir_parent_link:
                    files = [parent_file_detail] + files
            elif self.create_parent_links:
                files = [parent_file_detail] + files

            # Do generate a link to the parent directory
            full_path = self.make_index_file(files, 'Index of %s' % (folder,))

            if full_path:
                filename = os.path.basename(full_path)
                relative_name = os.path.join(folder, filename)
                indexes[folder] = FileDetail(full_path, relative_name)

        # This appends the index file at the end of the group of files
        # for each directory.
        new_list = []
        last_dirname = None
        for f in reversed(list(file_list)):
            if f.folder:
                relative_path = f.relative_path + '/'
            else:
                relative_path = f.relative_path
            dirname = os.path.dirname(relative_path)
            if dirname == '/':
                dirname = ''
            if dirname != last_dirname:
                index = indexes.pop(dirname, None)
                if index:
                    new_list.append(index)
                    last_dirname = dirname
            new_list.append(f)
        new_list.reverse()
        file_list.file_list = new_list

    def make_index_file(self, folder_links, title):
        """Writes an index into a file for pushing"""
        for file_details in folder_links:
            # Do not generate an index file if one exists already.
            # This may be the case when uploading other machine generated
            # content like python coverage info.
            if self.index_filename == file_details.filename:
                return
        index_content = self.generate_log_index(folder_links, title)
        tempdir = tempfile.mkdtemp()
        fd = open(os.path.join(tempdir, self.index_filename), 'w')
        fd.write(index_content)
        return os.path.join(tempdir, self.index_filename)

    def generate_log_index(self, folder_links, title):
        """Create an index of logfiles and links to them"""

        output = '<html><head><title>%s</title></head><body>\n' % title
        output += '<h1>%s</h1>\n' % title
        output += '<table><tr><th></th><th>Name</th><th>Last Modified</th>'
        output += '<th>Size</th></tr>'

        file_details_to_append = None
        for file_details in folder_links:
            output += '<tr>'
            output += (
                '<td><img alt="[ ]" title="%(m)s" src="%(i)s"></img></td>' % ({
                    'm': file_details.mimetype,
                    'i': get_mime_icon(file_details.mimetype,
                                       file_details.filename),
                }))
            filename = file_details.filename
            if file_details.folder:
                filename += '/'
            output += '<td><a href="%s">%s</a></td>' % (filename,
                                                        filename)
            output += '<td>%s</td>' % time.asctime(
                file_details.last_modified)
            size = sizeof_fmt(file_details.size, suffix='')
            output += '<td style="text-align: right">%s</td>' % size
            output += '</tr>\n'

            if (self.append_footer and
                self.append_footer in file_details.filename):
                file_details_to_append = file_details

        output += '</table>'

        if file_details_to_append:
            output += '<br /><hr />'
            try:
                with open(file_details_to_append.full_path, 'r') as f:
                    output += f.read()
            except IOError:
                logging.exception("Error opening file for appending")

        output += '</body></html>\n'
        return output


class DeflateFilter():
    chunk_size = 16384

    def __init__(self, infile):
        self.infile = infile
        self.encoder = zlib.compressobj()
        self.done = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.done:
            raise StopIteration()
        ret = b''
        while True:
            data = self.infile.read(self.chunk_size)
            if data:
                ret = self.encoder.compress(data)
                if ret:
                    break
            else:
                self.done = True
                ret = self.encoder.flush()
                break
        return ret


class Uploader():
    def __init__(self, cloud, container, prefix=None, delete_after=None,
                 public=True):
        if isinstance(cloud, dict):
            config = openstack.config.loader.OpenStackConfig().get_one(**cloud)
            self.cloud = openstack.connection.Connection(config=config)
        else:
            self.cloud = openstack.connect(cloud=cloud)
        self.container = container
        self.prefix = prefix or ''
        self.delete_after = delete_after

        sess = self.cloud.config.get_session()
        adapter = requests.adapters.HTTPAdapter(pool_maxsize=100)
        sess.mount('https://', adapter)

        if not self.cloud.get_container(self.container):
            self.cloud.create_container(name=self.container, public=public)
            self.cloud.update_container(
                name=self.container,
                headers={'X-Container-Meta-Web-Index': 'index.html'})
            # 'X-Container-Meta-Web-Listings': 'true'

            # The ceph radosgw swift implementation requires an
            # index.html at the root in order for any other indexes to
            # work.
            self.cloud.create_object(self.container,
                                     name='index.html',
                                     data='',
                                     content_type='text/html')
        self.url = os.path.join(self.cloud.object_store.get_endpoint(),
                                self.container, self.prefix)

    def upload(self, file_list):
        """Spin up thread pool to upload to swift"""
        num_threads = min(len(file_list), MAX_UPLOAD_THREADS)
        threads = []
        queue = queuelib.Queue()
        # add items to queue
        for f in file_list:
            queue.put(f)

        for x in range(num_threads):
            t = threading.Thread(target=self.post_thread, args=(queue,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    def post_thread(self, queue):
        while True:
            try:
                file_detail = queue.get_nowait()
                logging.debug("%s: processing job %s",
                              threading.current_thread(),
                              file_detail)
                self._post_file(file_detail)
            except requests.exceptions.RequestException:
                # Do our best to attempt to upload all the files
                logging.exception("Error posting file after multiple attempts")
                continue
            except IOError:
                # Do our best to attempt to upload all the files
                logging.exception("Error opening file")
                continue
            except queuelib.Empty:
                # No more work to do
                return

    @staticmethod
    def _is_text_type(mimetype):
        # We want to compress all text types.
        if mimetype.startswith('text/'):
            return True

        # Further compress types that typically contain text but are no
        # text sub type.
        compress_types = [
            'application/json',
            'image/svg+xml',
        ]
        if mimetype in compress_types:
            return True
        return False

    def _post_file(self, file_detail):
        relative_path = os.path.join(self.prefix, file_detail.relative_path)
        headers = {}
        if self.delete_after:
            headers['x-delete-after'] = str(self.delete_after)
        headers['content-type'] = file_detail.mimetype

        for attempt in range(1, POST_ATTEMPTS + 1):
            try:
                if not file_detail.folder:
                    if (file_detail.encoding is None and
                        self._is_text_type(file_detail.mimetype)):
                        headers['content-encoding'] = 'deflate'
                        data = DeflateFilter(open(file_detail.full_path, 'rb'))
                    else:
                        if file_detail.encoding:
                            headers['content-encoding'] = file_detail.encoding
                        data = open(file_detail.full_path, 'rb')
                else:
                    data = ''
                    relative_path = relative_path.rstrip('/')
                    if relative_path == '':
                        relative_path = '/'
                self.cloud.create_object(self.container,
                                         name=relative_path,
                                         data=data,
                                         **headers)
                break
            except requests.exceptions.RequestException:
                logging.exception(
                    "File posting error on attempt %d" % attempt)
                if attempt >= POST_ATTEMPTS:
                    raise


def run(cloud, container, files,
        indexes=True, parent_links=True, topdir_parent_link=False,
        partition=False, footer='index_footer.html', delete_after=15552000,
        prefix=None, public=True, dry_run=False):

    if prefix:
        prefix = prefix.lstrip('/')
    if partition and prefix:
        parts = prefix.split('/')
        if len(parts) > 1:
            container += '_' + parts[0]
            prefix = '/'.join(parts[1:])

    # Create the objects to make sure the arguments are sound.
    with FileList() as file_list:
        indexer = Indexer(create_parent_links=parent_links,
                          create_topdir_parent_link=topdir_parent_link,
                          append_footer=footer)

        # Scan the files.
        for file_path in files:
            file_list.add(file_path)

        # (Possibly) make indexes.
        if indexes:
            indexer.make_indexes(file_list)

        logging.debug("List of files prepared to upload:")
        for x in file_list:
            logging.debug(x)

        # Do no connect to swift or do any uploading in a dry run
        if dry_run:
            # No URL is known, so return nothing
            return

        # Upload.
        uploader = Uploader(cloud, container, prefix, delete_after,
                            public)
        uploader.upload(file_list)
        return uploader.url


def ansible_main():
    module = AnsibleModule(
        argument_spec=dict(
            cloud=dict(required=True, type='raw'),
            container=dict(required=True, type='str'),
            files=dict(required=True, type='list'),
            partition=dict(type='bool', default=False),
            indexes=dict(type='bool', default=True),
            parent_links=dict(type='bool', default=True),
            topdir_parent_link=dict(type='bool', default=False),
            public=dict(type='bool', default=True),
            footer=dict(type='str'),
            delete_after=dict(type='int'),
            prefix=dict(type='str'),
        )
    )

    p = module.params
    url = run(p.get('cloud'), p.get('container'), p.get('files'),
              indexes=p.get('indexes'),
              parent_links=p.get('parent_links'),
              topdir_parent_link=p.get('topdir_parent_link'),
              partition=p.get('partition'),
              footer=p.get('footer'),
              delete_after=p.get('delete_after', 15552000),
              prefix=p.get('prefix'),
              public=p.get('public'))

    module.exit_json(changed=True,
                     url=url)


def cli_main():
    parser = argparse.ArgumentParser(
        description="Upload files to swift"
    )
    parser.add_argument('--verbose', action='store_true',
                        help='show debug information')
    parser.add_argument('--no-indexes', action='store_true',
                        help='do not generate any indexes at all')
    parser.add_argument('--no-parent-links', action='store_true',
                        help='do not include links back to a parent dir')
    parser.add_argument('--create-topdir-parent-link', action='store_true',
                        help='include a link in the root directory of the '
                             'files to the parent directory which may be the '
                             'index of all results')
    parser.add_argument('--no-public', action='store_true',
                        help='do not create the container as public')
    parser.add_argument('--partition', action='store_true',
                        help='partition the prefix into multiple containers')
    parser.add_argument('--append-footer', default='index_footer.html',
                        help='when generating an index, if the given file is '
                             'present in a directory, append it to the index '
                             '(set to "none" to disable)')
    parser.add_argument('--delete-after', default=15552000,
                        help='Number of seconds to delete object after '
                             'upload. Default is 6 months (15552000 seconds) '
                             'and if set to 0 X-Delete-After will not be set',
                        type=int)
    parser.add_argument('--prefix',
                        help='Prepend this path to the object names when '
                             'uploading')
    parser.add_argument('--dry-run', action='store_true',
                        help='do not attempt to create containers or upload, '
                             'useful with --verbose for debugging')
    parser.add_argument('cloud',
                        help='Name of the cloud to use when uploading')
    parser.add_argument('container',
                        help='Name of the container to use when uploading')
    parser.add_argument('files', nargs='+',
                        help='the file(s) to upload with recursive glob '
                        'matching when supplied as a string')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        # Set requests log level accordingly
        logging.getLogger("requests").setLevel(logging.DEBUG)
        logging.captureWarnings(True)

    append_footer = args.append_footer
    if append_footer.lower() == 'none':
        append_footer = None

    url = run(args.cloud, args.container, args.files,
              indexes=not args.no_indexes,
              parent_links=not args.no_parent_links,
              topdir_parent_link=args.create_topdir_parent_link,
              partition=args.partition,
              footer=append_footer,
              delete_after=args.delete_after,
              prefix=args.prefix,
              public=not args.no_public,
              dry_run=args.dry_run)
    print(url)


if __name__ == '__main__':
    # Avoid unactionable warnings
    requestsexceptions.squelch_warnings(
        requestsexceptions.InsecureRequestWarning)

    if sys.stdin.isatty():
        cli_main()
    else:
        ansible_main()
