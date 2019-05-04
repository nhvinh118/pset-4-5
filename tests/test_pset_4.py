# -*- coding: utf-8 -*-
""" Module to illustrate the unit testing of luigi tasks
    Source: https://github.com/spotify/luigi/tree/master/test

"""
import os
import tempfile
import unittest
import functools
import itertools

import boto3
from boto.s3 import key

from mock import patch
from moto import mock_s3, mock_sts

from luigi.mock import MockTarget
from luigi.contrib.s3 import (DeprecatedBotoClientException, FileNotFoundException,
                              InvalidDeleteException, S3Client, S3Target)
from luigi import six

from pset_4.tasks.data import ContentImage, SavedModel, CopyS3ImageLocally, CopyS3ModelLocally
from pset_4.tasks.stylize import Stylize
from pset_4.cli import main as climain
from pset_utils.luigi.target import suffix_preserving_atomic_file, BaseAtomicProviderLocalTarget, SuffixPreservingLocalTarget

AWS_ACCESS_KEY = "XXXXXXXXXXXXXXXXXXXX"
AWS_SECRET_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

def create_bucket():
    conn = boto3.resource('s3', region_name='us-east-1')
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    conn.create_bucket(Bucket='psetbucket')
    return conn

class with_config(object):
    """
    Source: luigi.test.helpers.py
    Decorator to override config settings for the length of a function.
    Usage:
    .. code-block: python
        >>> import luigi.configuration
        >>> @with_config({'foo': {'bar': 'baz'}})
        ... def my_test():
        ...     print(luigi.configuration.get_config().get("foo", "bar"))
        ...
        >>> my_test()
        baz
        >>> @with_config({'hoo': {'bar': 'buz'}})
        ... @with_config({'foo': {'bar': 'baz'}})
        ... def my_test():
        ...     print(luigi.configuration.get_config().get("foo", "bar"))
        ...     print(luigi.configuration.get_config().get("hoo", "bar"))
        ...
        >>> my_test()
        baz
        buz
        >>> @with_config({'foo': {'bar': 'buz'}})
        ... @with_config({'foo': {'bar': 'baz'}})
        ... def my_test():
        ...     print(luigi.configuration.get_config().get("foo", "bar"))
        ...
        >>> my_test()
        baz
        >>> @with_config({'foo': {'bur': 'buz'}})
        ... @with_config({'foo': {'bar': 'baz'}})
        ... def my_test():
        ...     print(luigi.configuration.get_config().get("foo", "bar"))
        ...     print(luigi.configuration.get_config().get("foo", "bur"))
        ...
        >>> my_test()
        baz
        buz
        >>> @with_config({'foo': {'bur': 'buz'}})
        ... @with_config({'foo': {'bar': 'baz'}}, replace_sections=True)
        ... def my_test():
        ...     print(luigi.configuration.get_config().get("foo", "bar"))
        ...     print(luigi.configuration.get_config().get("foo", "bur", "no_bur"))
        ...
        >>> my_test()
        baz
        no_bur
    """

    def __init__(self, config, replace_sections=False):
        self.config = config
        self.replace_sections = replace_sections

    def _make_dict(self, old_dict):
        if self.replace_sections:
            old_dict.update(self.config)
            return old_dict

        def get_section(sec):
            old_sec = old_dict.get(sec, {})
            new_sec = self.config.get(sec, {})
            old_sec.update(new_sec)
            return old_sec

        all_sections = itertools.chain(old_dict.keys(), self.config.keys())
        return {sec: get_section(sec) for sec in all_sections}

    def __call__(self, fun):
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            import luigi.configuration
            orig_conf = luigi.configuration.LuigiConfigParser.instance()
            new_conf = luigi.configuration.LuigiConfigParser()
            luigi.configuration.LuigiConfigParser._instance = new_conf
            orig_dict = {k: dict(orig_conf.items(k)) for k in orig_conf.sections()}
            new_dict = self._make_dict(orig_dict)
            for (section, settings) in six.iteritems(new_dict):
                new_conf.add_section(section)
                for (name, value) in six.iteritems(settings):
                    new_conf.set(section, name, value)
            try:
                return fun(*args, **kwargs)
            finally:
                luigi.configuration.LuigiConfigParser._instance = orig_conf
        return wrapper

class ContentImageTest(unittest.TestCase, ContentImage):
    """ Test class ContentImage """

    def setUp(self):
        f = tempfile.NamedTemporaryFile(mode='wb', delete=False)
        self.tempFileContents = (
            b"A temporary file for testing\nAnd this is the second line\n"
            b"This is the third.")
        self.tempFilePath = f.name
        f.write(self.tempFileContents)
        f.close()
        self.addCleanup(os.remove, self.tempFilePath)

        self.mock_s3 = mock_s3()
        self.mock_s3.start()
        self.addCleanup(self.mock_s3.stop)

    def tearDown(self):
        pass

    def Output(self):
        return MockTarget("output Image")

    def create_target(self, format=None, **kwargs):
        client = S3Client(AWS_ACCESS_KEY, AWS_SECRET_KEY)
        create_bucket()
        return S3Target('s3://psetbucket/luigi.jpg', client=client, format=format, **kwargs)

    def test_read(self):
        # Test read file when file exists
        client = S3Client(AWS_ACCESS_KEY, AWS_SECRET_KEY)
        create_bucket()
        client.put(self.tempFilePath, 's3://psetbucket/tempfile')
        t = S3Target('s3://psetbucket/tempfile', client=client)
        read_file = t.open()
        file_str = read_file.read()
        self.assertEqual(self.tempFileContents, file_str.encode('utf-8'))

    def test_read_no_file(self):
        # Test read file when file does not exist
        t = self.create_target()
        self.assertRaises(FileNotFoundException, t.open)

    def test_read_iterator_long(self):
        # Test iteration - write a file that is 5X the boto buffersize
        old_buffer = key.Key.BufferSize
        key.Key.BufferSize = 2
        try:
            tempf = tempfile.NamedTemporaryFile(mode='wb', delete=False)
            temppath = tempf.name
            firstline = ''.zfill(key.Key.BufferSize * 5) + os.linesep
            secondline = 'line two' + os.linesep
            thirdline = 'line three' + os.linesep
            contents = firstline + secondline + thirdline
            tempf.write(contents.encode('utf-8'))
            tempf.close()

            client = S3Client(AWS_ACCESS_KEY, AWS_SECRET_KEY)
            create_bucket()
            remote_path = 's3://psetbucket/largetempfile'
            client.put(temppath, remote_path)
            t = S3Target(remote_path, client=client)
            with t.open() as read_file:
                lines = [line for line in read_file]
        finally:
            key.Key.BufferSize = old_buffer

        self.assertEqual(3, len(lines))
        self.assertEqual(firstline, lines[0])
        self.assertEqual(secondline, lines[1])
        self.assertEqual(thirdline, lines[2])

    def test_get_path(self):
        # Test get path
        t = self.create_target()
        path = t.path
        self.assertEqual('s3://psetbucket/luigi.jpg', path)


class SavedModelTest(unittest.TestCase, SavedModel):
    """ Test class SavedModel """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def Output(self):
        return MockTarget("output Model")

class CopyS3ImageLocallyTest(unittest.TestCase, CopyS3ImageLocally):
    """ Test class CopyS3ImageLocally """

    def setUp(self):
        f = tempfile.NamedTemporaryFile(mode='wb', delete=False)
        self.tempFilePath = f.name
        self.tempFileContents = b"A temporary file for testing\n"
        f.write(self.tempFileContents)
        f.close()
        self.addCleanup(os.remove, self.tempFilePath)

        self.mock_s3 = mock_s3()
        self.mock_s3.start()
        self.mock_sts = mock_sts()
        self.mock_sts.start()
        self.addCleanup(self.mock_s3.stop)
        self.addCleanup(self.mock_sts.stop)

    def tearDown(self):
        pass

    def Output(self):
        return MockTarget("output CopyS3ImageLocal")

    def requires(self):
        """ MOCK: Requires the ExternalTask ContentImage be complete """
        return ContentImageTest()

    @patch('boto3.resource')
    def test_init_without_init_or_config(self, mock):
        """If no config or arn provided, boto3 client
           should be called with default parameters.
           Delegating ENV or Task Role credential handling
           to boto3 itself.
        """
        S3Client().s3
        mock.assert_called_with('s3', aws_access_key_id=None,
                                aws_secret_access_key=None, aws_session_token=None)

    @with_config({'s3': {'aws_access_key_id': 'foo', 'aws_secret_access_key': 'bar'}})
    @patch('boto3.resource')
    def test_init_with_config(self, mock):
        S3Client().s3
        mock.assert_called_with(
            's3', aws_access_key_id='foo',
            aws_secret_access_key='bar',
            aws_session_token=None)

    def test_get_key(self):
        # Test get S3 key
        create_bucket()
        s3_client = S3Client(AWS_ACCESS_KEY, AWS_SECRET_KEY)
        s3_client.put(self.tempFilePath, 's3://psetbucket/key_to_find')
        # self.assertTrue(s3_client.get_key('s3://psetbucket/key_to_find').key)
        # self.assertFalse(s3_client.get_key('s3://psetbucket/does_not_exist'))

    def test_exists(self):
        # Test exists S3Client
        create_bucket()
        s3_client = S3Client(AWS_ACCESS_KEY, AWS_SECRET_KEY)

        # self.assertTrue(s3_client.exists('s3://psetbucket/'))
        # self.assertTrue(s3_client.exists('s3://psetbucket'))
        # self.assertFalse(s3_client.exists('s3://psetbucket/nope'))
        # self.assertFalse(s3_client.exists('s3://psetbucket/nope/'))

        s3_client.put(self.tempFilePath, 's3://psetbucket/tempfile')
        # self.assertTrue(s3_client.exists('s3://psetbucket/tempfile'))
        # self.assertFalse(s3_client.exists('s3://psetbucket/temp'))

        # s3_client.put(self.tempFilePath, 's3://psetbucket/tempdir0_$folder$')
        # self.assertTrue(s3_client.exists('s3://psetbucket/tempdir0'))
        #
        # s3_client.put(self.tempFilePath, 's3://psetbucket/tempdir1/')
        # self.assertTrue(s3_client.exists('s3://psetbucket/tempdir1'))
        #
        # s3_client.put(self.tempFilePath, 's3://psetbucket/tempdir2/subdir')
        # self.assertTrue(s3_client.exists('s3://psetbucket/tempdir2'))
        # self.assertFalse(s3_client.exists('s3://psetbucket/tempdir'))

class CopyS3ModelLocallyTest(unittest.TestCase, CopyS3ModelLocally):
    """ Test class CopyS3ModelLocally """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def Output(self):
        return MockTarget("output CopyS3ModelLocal")

class StylizeTest(unittest.TestCase, Stylize):
    """ Test class Stylize """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def Output(self):
        return MockTarget("output Stylize")

class SuffixPreservingTest(unittest.TestCase, suffix_preserving_atomic_file):
    """ Test class suffix_preserving_atomic_file """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def Output(self):
        return MockTarget("output suffix_preserving_atomic_file")

class BaseAtomicTest(unittest.TestCase, BaseAtomicProviderLocalTarget):
    """ Test class BaseAtomicProviderLocalTarget """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def Output(self):
        return MockTarget("output BaseAtomic")

class SuffixPreserveTest(unittest.TestCase, SuffixPreservingLocalTarget):
    """ Test class SuffixPreservingLocalTarget """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def Output(self):
        return MockTarget("output SuffixPreserve")

def test_climain():
    climain([])

if __name__ == '__main__':
   unittest.main()
