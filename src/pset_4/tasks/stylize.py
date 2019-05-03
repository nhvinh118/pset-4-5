# -*- coding: utf-8 -*-
"""Module to perform the neural style operation
   Command:

   python neural_style/neural_style.py eval --content-image </path/to/content/image> \
	--model </path/to/saved/model> --output-image </path/to/output/image> --cuda 0

   Implements Class Stylize as a Luigi Task to call 'neural_style.stylize'

"""
import argparse
import os

import luigi
from luigi import Task

from neural_style.neural_style import stylize
from pset_utils.luigi.target import SuffixPreservingLocalTarget
from pset_4.tasks.data import CopyS3ModelLocally, CopyS3ImageLocally

class Stylize(Task):
 
	LOCAL_MODEL_ROOT = os.path.join('data', 'model/')
	LOCAL_IMAGE_ROOT = os.path.join('data', 'image/')

	def __init__(self):
		pass

	def requires(self):
		"""Ensures that image and model have been copied locally """

		return {
			'image': CopyS3ImageLocally(),
			'model': CopyS3ModelLocally()
		}

	def output(self):
		# Set output file for new image
		iloc = self.LOCAL_IMAGE_ROOT + args.image
		LocalTargetSImg = SuffixPreservingLocalTarget(iloc)
		return LocalTargetSImg

	def run(self):
		# Perform the stylize operation
		inputs = self.input()
		with self.output().temporary_path() as temp_output_path:
			# Reset args
			args.content_image = inputs['image'].path
			args.output_image = temp_output_path
			args.model = inputs['model'].path
			args.export_onnx = ''
			# Execute stylize
			stylize(args)

# UNIT TEST: To be removed
if __name__ == "__main__":
	pass
