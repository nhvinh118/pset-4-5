# -*- coding: utf-8 -*-
""" This module supplements Luigi's atomic writing within its Target classes. 
    The subclassed method preserves the suffix of the output target in the temporary file. 
 
"""
import io
import os
import random
import traceback
from contextlib import contextmanager

import luigi
from luigi.local_target import LocalTarget, atomic_file
from luigi.format import FileWrapper, get_default_format

class suffix_preserving_atomic_file(atomic_file):
	""" This class provides the method to create the name of a temporary path, preserving the extension
	"""
	def __init__(self, path=''):
		super().__init__(path)
	
	def __enter__(self, path=''):
		"""Method to return itself """

		return self
		 
	def generate_tmp_path(self, path=''):
		"""Method to override atomic_file """

		dirname, fname = os.path.split(path)

		try:
			basename, ext = fname.split('.', 1)
		except ValueError:
			ext = ''
	 
		self.__gen_tmppath = dirname + '/' + basename + '-luigi-tmp-%09d' % random.randrange(0, 1e10) + '.' + ext

		return self.__gen_tmppath

class BaseAtomicProviderLocalTarget(LocalTarget):
	"""This provides the base atomic provider class with 2 methods:
	- open()
	- temporary_path()
	"""

	# Allow some composability of atomic handling
	atomic_provider = atomic_file

	def __init__(self, path=None, format=None, is_tmp=False):
		if format is None:
			format = get_default_format()
		super(LocalTarget, self).__init__(path)
		self.format = format
	
	def open(self, mode='r'):
		# leverage super() 
		my_super = super(LocalTarget, self).__init__(self.path)

		try:
			# Modify LocalTarget.open() to use atomic_provider rather than atomic_file
			rwmode = mode.replace('b', '').replace('t', '')
			if rwmode == 'w':
				self.makedirs()
				ipath = self.format.pipe_writer(self.atomic_provider(self.path))
				return ipath
			elif rwmode == 'r':
				fileobj = FileWrapper(io.BufferedReader(io.FileIO(self.path, mode)))
				return self.format.pipe_reader(fileobj)
			else:
				raise Exception("mode must be 'r' or 'w' (got: %s)" % mode)
		except Exception:
			traceback.print_exc()
		
	@contextmanager
	def temporary_path(self):
		lpath = self.path
		self.makedirs()
		with self.atomic_provider(lpath) as af:
			yield af.tmp_path
	
	def xxtemporary_path(self):
		# Mock
		self.makedirs()
		af = self.atomic_provider(self.path) 
		return af


class SuffixPreservingLocalTarget(BaseAtomicProviderLocalTarget):
	"""This class returns the temporary path
	"""

	# Set atomic_provider to the suffix preserving method
	atomic_provider = suffix_preserving_atomic_file


# UNIT TEST: To be removed
if __name__ == "__main__": 
	pass