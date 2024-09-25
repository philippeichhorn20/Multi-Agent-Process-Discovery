import pm4py
import pandas as pd
from fastapi import UploadFile
import os

class NetStorer(object):

	def __init__(self):
		self.xes_path = None
		self.log = None
		self.df = None

	@classmethod
	async def create(cls, file: UploadFile):
		instance = cls()  # Create an instance
		file_content = await file.read()
		temp_file_path = 'temp_log.xes'
		with open(temp_file_path, 'wb') as temp_file:
			temp_file.write(file_content)
		instance.xes_path = temp_file_path
		instance.log = pm4py.read_xes(file_path=instance.xes_path)
		instance.df = pm4py.convert_to_dataframe(instance.log)
		return instance  # Return the instance

	def close(self):
		if os.path.exists(self.xes_path):
			os.remove(self.xes_path)