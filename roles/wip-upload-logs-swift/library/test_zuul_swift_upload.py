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

import unittest
from .zuul_swift_upload import FileList, Indexer
import os

from bs4 import BeautifulSoup

FIXTURE_DIR = os.path.join(os.path.dirname(__file__),
                           'test-fixtures')


class TestFileList(unittest.TestCase):

    def assert_files(self, result, files):
        self.assertEqual(len(result), len(files))
        for expected, received in zip(files, result):
            self.assertEqual(expected[0], received.relative_path)
            if expected[0] and expected[0][-1] == '/':
                efilename = os.path.split(
                    os.path.dirname(expected[0]))[1] + '/'
            else:
                efilename = os.path.split(expected[0])[1]
            self.assertEqual(efilename, received.filename)
            if received.folder:
                if received.full_path is not None and expected[0] != '':
                    self.assertTrue(os.path.isdir(received.full_path))
            else:
                self.assertTrue(os.path.isfile(received.full_path))
            self.assertEqual(expected[1], received.mimetype)
            self.assertEqual(expected[2], received.encoding)

    def find_file(self, file_list, path):
        for f in file_list:
            if f.relative_path == path:
                return f

    def test_single_dir_trailing_slash(self):
        '''Test a single directory with a trailing slash'''
        fl = FileList()
        fl.add(os.path.join(FIXTURE_DIR, 'logs/'))
        self.assert_files(fl, [
            ('', 'application/directory', None),
            ('controller', 'application/directory', None),
            ('zuul-info', 'application/directory', None),
            ('job-output.json', 'application/json', None),
            ('controller/subdir', 'application/directory', None),
            ('controller/compressed.gz', 'text/plain', 'gzip'),
            ('controller/journal.xz', 'text/plain', 'xz'),
            ('controller/service_log.txt', 'text/plain', None),
            ('controller/syslog', 'text/plain', None),
            ('controller/subdir/subdir.txt', 'text/plain', None),
            ('zuul-info/inventory.yaml', 'text/plain', None),
            ('zuul-info/zuul-info.controller.txt', 'text/plain', None),
        ])

    def test_single_dir(self):
        '''Test a single directory without a trailing slash'''
        fl = FileList()
        fl.add(os.path.join(FIXTURE_DIR, 'logs'))
        self.assert_files(fl, [
            ('', 'application/directory', None),
            ('logs', 'application/directory', None),
            ('logs/controller', 'application/directory', None),
            ('logs/zuul-info', 'application/directory', None),
            ('logs/job-output.json', 'application/json', None),
            ('logs/controller/subdir', 'application/directory', None),
            ('logs/controller/compressed.gz', 'text/plain', 'gzip'),
            ('logs/controller/journal.xz', 'text/plain', 'xz'),
            ('logs/controller/service_log.txt', 'text/plain', None),
            ('logs/controller/syslog', 'text/plain', None),
            ('logs/controller/subdir/subdir.txt', 'text/plain', None),
            ('logs/zuul-info/inventory.yaml', 'text/plain', None),
            ('logs/zuul-info/zuul-info.controller.txt', 'text/plain', None),
        ])

    def test_single_file(self):
        '''Test a single file'''
        fl = FileList()
        fl.add(os.path.join(FIXTURE_DIR,
                            'logs/zuul-info/inventory.yaml'))
        self.assert_files(fl, [
            ('', 'application/directory', None),
            ('inventory.yaml', 'text/plain', None),
        ])

    def test_index_files(self):
        '''Test index generation'''
        fl = FileList()
        fl.add(os.path.join(FIXTURE_DIR, 'logs'))
        ix = Indexer()
        fl = ix.make_indexes(fl)

        self.assert_files(fl, [
            ('', 'application/directory', None),
            ('index.html', 'text/html', None),
            ('logs', 'application/directory', None),
            ('logs/controller', 'application/directory', None),
            ('logs/zuul-info', 'application/directory', None),
            ('logs/job-output.json', 'application/json', None),
            ('logs/index.html', 'text/html', None),
            ('logs/controller/subdir', 'application/directory', None),
            ('logs/controller/compressed.gz', 'text/plain', 'gzip'),
            ('logs/controller/journal.xz', 'text/plain', 'xz'),
            ('logs/controller/service_log.txt', 'text/plain', None),
            ('logs/controller/syslog', 'text/plain', None),
            ('logs/controller/index.html', 'text/html', None),
            ('logs/controller/subdir/subdir.txt', 'text/plain', None),
            ('logs/controller/subdir/index.html', 'text/html', None),
            ('logs/zuul-info/inventory.yaml', 'text/plain', None),
            ('logs/zuul-info/zuul-info.controller.txt', 'text/plain', None),
            ('logs/zuul-info/index.html', 'text/html', None),
        ])

        top_index = self.find_file(fl, 'index.html')
        page = open(top_index.full_path).read()
        page = BeautifulSoup(page, 'html.parser')
        rows = page.find_all('tr')[1:]

        self.assertEqual(len(rows), 1)

        self.assertEqual(rows[0].find('a').get('href'), 'logs/')
        self.assertEqual(rows[0].find('a').text, 'logs/')

        subdir_index = self.find_file(fl, 'logs/controller/subdir/index.html')
        page = open(subdir_index.full_path).read()
        page = BeautifulSoup(page, 'html.parser')
        rows = page.find_all('tr')[1:]
        self.assertEqual(rows[0].find('a').get('href'), '../')
        self.assertEqual(rows[0].find('a').text, '../')

        self.assertEqual(rows[1].find('a').get('href'), 'subdir.txt')
        self.assertEqual(rows[1].find('a').text, 'subdir.txt')

    def test_index_files_trailing_slash(self):
        '''Test index generation with a trailing slash'''
        fl = FileList()
        fl.add(os.path.join(FIXTURE_DIR, 'logs/'))
        ix = Indexer()
        fl = ix.make_indexes(fl)

        self.assert_files(fl, [
            ('', 'application/directory', None),
            ('controller', 'application/directory', None),
            ('zuul-info', 'application/directory', None),
            ('job-output.json', 'application/json', None),
            ('index.html', 'text/html', None),
            ('controller/subdir', 'application/directory', None),
            ('controller/compressed.gz', 'text/plain', 'gzip'),
            ('controller/journal.xz', 'text/plain', 'xz'),
            ('controller/service_log.txt', 'text/plain', None),
            ('controller/syslog', 'text/plain', None),
            ('controller/index.html', 'text/html', None),
            ('controller/subdir/subdir.txt', 'text/plain', None),
            ('controller/subdir/index.html', 'text/html', None),
            ('zuul-info/inventory.yaml', 'text/plain', None),
            ('zuul-info/zuul-info.controller.txt', 'text/plain', None),
            ('zuul-info/index.html', 'text/html', None),
        ])

        top_index = self.find_file(fl, 'index.html')
        page = open(top_index.full_path).read()
        page = BeautifulSoup(page, 'html.parser')
        rows = page.find_all('tr')[1:]

        self.assertEqual(len(rows), 3)

        self.assertEqual(rows[0].find('a').get('href'), 'controller/')
        self.assertEqual(rows[0].find('a').text, 'controller/')

        self.assertEqual(rows[1].find('a').get('href'), 'zuul-info/')
        self.assertEqual(rows[1].find('a').text, 'zuul-info/')

        subdir_index = self.find_file(fl, 'controller/subdir/index.html')
        page = open(subdir_index.full_path).read()
        page = BeautifulSoup(page, 'html.parser')
        rows = page.find_all('tr')[1:]
        self.assertEqual(rows[0].find('a').get('href'), '../')
        self.assertEqual(rows[0].find('a').text, '../')

        self.assertEqual(rows[1].find('a').get('href'), 'subdir.txt')
        self.assertEqual(rows[1].find('a').text, 'subdir.txt')

    def test_topdir_parent_link(self):
        '''Test index generation creates topdir parent link'''
        fl = FileList()
        fl.add(os.path.join(FIXTURE_DIR, 'logs/'))
        ix = Indexer(create_parent_links=True,
                     create_topdir_parent_link=True)
        fl = ix.make_indexes(fl)

        self.assert_files(fl, [
            ('', 'application/directory', None),
            ('controller', 'application/directory', None),
            ('zuul-info', 'application/directory', None),
            ('job-output.json', 'application/json', None),
            ('index.html', 'text/html', None),
            ('controller/subdir', 'application/directory', None),
            ('controller/compressed.gz', 'text/plain', 'gzip'),
            ('controller/journal.xz', 'text/plain', 'xz'),
            ('controller/service_log.txt', 'text/plain', None),
            ('controller/syslog', 'text/plain', None),
            ('controller/index.html', 'text/html', None),
            ('controller/subdir/subdir.txt', 'text/plain', None),
            ('controller/subdir/index.html', 'text/html', None),
            ('zuul-info/inventory.yaml', 'text/plain', None),
            ('zuul-info/zuul-info.controller.txt', 'text/plain', None),
            ('zuul-info/index.html', 'text/html', None),
        ])

        top_index = self.find_file(fl, 'index.html')
        page = open(top_index.full_path).read()
        page = BeautifulSoup(page, 'html.parser')
        rows = page.find_all('tr')[1:]

        self.assertEqual(len(rows), 4)

        self.assertEqual(rows[0].find('a').get('href'), '../')
        self.assertEqual(rows[0].find('a').text, '../')

        self.assertEqual(rows[1].find('a').get('href'), 'controller/')
        self.assertEqual(rows[1].find('a').text, 'controller/')

        self.assertEqual(rows[2].find('a').get('href'), 'zuul-info/')
        self.assertEqual(rows[2].find('a').text, 'zuul-info/')

        subdir_index = self.find_file(fl, 'controller/subdir/index.html')
        page = open(subdir_index.full_path).read()
        page = BeautifulSoup(page, 'html.parser')
        rows = page.find_all('tr')[1:]
        self.assertEqual(rows[0].find('a').get('href'), '../')
        self.assertEqual(rows[0].find('a').text, '../')

        self.assertEqual(rows[1].find('a').get('href'), 'subdir.txt')
        self.assertEqual(rows[1].find('a').text, 'subdir.txt')

    def test_no_parent_links(self):
        '''Test index generation creates topdir parent link'''
        fl = FileList()
        fl.add(os.path.join(FIXTURE_DIR, 'logs/'))
        ix = Indexer(create_parent_links=False,
                     create_topdir_parent_link=False)
        fl = ix.make_indexes(fl)

        self.assert_files(fl, [
            ('', 'application/directory', None),
            ('controller', 'application/directory', None),
            ('zuul-info', 'application/directory', None),
            ('job-output.json', 'application/json', None),
            ('index.html', 'text/html', None),
            ('controller/subdir', 'application/directory', None),
            ('controller/compressed.gz', 'text/plain', 'gzip'),
            ('controller/journal.xz', 'text/plain', 'xz'),
            ('controller/service_log.txt', 'text/plain', None),
            ('controller/syslog', 'text/plain', None),
            ('controller/index.html', 'text/html', None),
            ('controller/subdir/subdir.txt', 'text/plain', None),
            ('controller/subdir/index.html', 'text/html', None),
            ('zuul-info/inventory.yaml', 'text/plain', None),
            ('zuul-info/zuul-info.controller.txt', 'text/plain', None),
            ('zuul-info/index.html', 'text/html', None),
        ])

        top_index = self.find_file(fl, 'index.html')
        page = open(top_index.full_path).read()
        page = BeautifulSoup(page, 'html.parser')
        rows = page.find_all('tr')[1:]

        self.assertEqual(len(rows), 3)

        self.assertEqual(rows[0].find('a').get('href'), 'controller/')
        self.assertEqual(rows[0].find('a').text, 'controller/')

        self.assertEqual(rows[1].find('a').get('href'), 'zuul-info/')
        self.assertEqual(rows[1].find('a').text, 'zuul-info/')

        subdir_index = self.find_file(fl, 'controller/subdir/index.html')
        page = open(subdir_index.full_path).read()
        page = BeautifulSoup(page, 'html.parser')
        rows = page.find_all('tr')[1:]

        self.assertEqual(rows[0].find('a').get('href'), 'subdir.txt')
        self.assertEqual(rows[0].find('a').text, 'subdir.txt')
