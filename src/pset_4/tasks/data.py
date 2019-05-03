# -*- coding: utf-8 -*-
"""This module implements the features to execute the "stylizing" command against objects in AWS,
   using luigi pipelines:

   python neural_style/neural_style.py eval --content-image </path/to/content/image> --model \
		 </path/to/saved/model> --output-image </path/to/output/image> --cuda 0

   The command above stylizes an image given the pre-trained model - considering the dependency graph:

   1) A model on S3 (s3://cscie29-data/pset4/model/rain_princess.pth)
   2) An input image on S3 (s3://cscie29-data/pset4/data/luigi.jpg)

"""
import os
import traceback

# Luigi
import luigi
from luigi import ExternalTask, Parameter, Task
from luigi.contrib.s3 import S3Target
# AWS 
import boto3

class ContentImage(ExternalTask):
	""" Create a Luigi External Task that returns the S3 target object of the image 
	"""

	IMAGE_ROOT = "s3://cscie29-data/pset4/data/" # Image root S3 path

	image = Parameter(default="luigi.jpg") # Filename of the image under the root s3 path

	def output(self):
		# return the S3Target of the image
		floc = self.IMAGE_ROOT + self.param_kwargs["image"]
		S3Targetimage = S3Target(floc, format=luigi.format.Nop)
		
		return S3Targetimage

class SavedModel(ExternalTask):
	""" Create a Luigi External Task that returns the S3 target object of the model
	"""

	MODEL_ROOT = "s3://cscie29-data/pset4/model/"  # Model root S3 path

	model = Parameter(default="rain_princess.pth") # Filename of the model

	def output(self):
		# return the S3Target of the model
		mloc = self.MODEL_ROOT + self.param_kwargs["model"]
		S3Targetmodel = S3Target(mloc, format=luigi.format.Nop)

		return S3Targetmodel

class CopyS3ModelLocally(Task):
	""" Copy the model from S3 to local folder
	"""

	LOCAL_MODEL_ROOT = os.path.join('data', 'model/') # set local folder for model
	
	model = SavedModel().param_kwargs["model"] # get 'model' from luigi Parameter

	def requires(self):
		"""Requires the ExternalTask "SavedModel" be complete
		i.e. the model must exist on S3 in order to copy it locally"""

		return SavedModel()

	def output(self):
		"""Set output file for model"""

		mloc = self.LOCAL_MODEL_ROOT + self.model
		LocalTargetmodel = luigi.LocalTarget(mloc)
		LocalTargetmodel.makedirs()
		return LocalTargetmodel

	def run(self):
		""" Copy model in S3 to local folder """

		fromS3 = self.input().path
		toLocal = self.output().path

		try:
			# Get <bucket, key> from path
			myS3Client = self.input().fs
			src_bucket, src_key = myS3Client._path_to_bucket_and_key(fromS3)
			# Use S3Client to copy file to local
			myS3 = boto3.client ('s3')
			myS3.download_file(src_bucket,src_key,toLocal)

		except Exception:
			traceback.print_exc()

class CopyS3ImageLocally(Task):
	""" Copy the image from S3 to local folder
	"""

	LOCAL_IMAGE_ROOT = os.path.join('data', 'image/') # set local folder for image
	
	image = ContentImage().param_kwargs["image"] # get image name from luigi Parameter

	def requires(self):
		""" Requires the ExternalTask ContentImage be complete
		i.e. the image must exist on S3 in order to copy it locally"""

		return ContentImage()

	def output(self):
		"""Set output file for image"""

		iloc = self.LOCAL_IMAGE_ROOT + self.image
		LocalTargetimage = luigi.LocalTarget(iloc)
		LocalTargetimage.makedirs()
		return LocalTargetimage

	def run(self):
		""" Copy image in S3 to local folder """

		fromS3 = self.input().path
		toLocal = self.output().path

		try:
			# Get <bucket, key> from path
			myS3Client = self.input().fs
			src_bucket, src_key = myS3Client._path_to_bucket_and_key(fromS3)
			# Use S3Client to copy file to local
			myS3 = boto3.client ('s3')
			myS3.download_file(src_bucket,src_key,toLocal)

		except Exception:
			traceback.print_exc()


# UNIT TEST: To be removed
if __name__ == "__main__": 
	pass