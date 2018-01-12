import csv
from datetime import datetime
import os
import sys


DATA_STRUCTURE_BASEPATH = os.path.join(os.path.dirname(__file__), 'datastructure')
CSV_FILENAME = 'watts-%Y-%m-%d-c.csv'


class ElectricityDataWriter:
	# Number of rows to cache before writing to file
	BUFFER_SIZE = 5

	def __init__(self, data_structure_basepath):
		self.data_structure_basepath = data_structure_basepath
		self._file = None
		self._writer = None
		self._row_buffer = []

	def _get_filepath(self, _datetime):
		return os.path.join(self.data_structure_basepath, _datetime.strftime('%Y/%m/%Y-%m-%d'), _datetime.strftime(CSV_FILENAME))

	def _open_file(self, filepath):
		return open(filepath, 'a', newline='')

	def _handle_file_object(self, _datetime):	
		filepath = self._get_filepath(_datetime)
		file_exists = os.path.isfile(filepath)

		if not file_exists:
			os.makedirs(os.path.dirname(filepath), exist_ok=True)
		
		if self._file is None:
			self._file = self._open_file(filepath)
		elif self._file.name != filepath:
			self._file.close()
			self._file = self._open_file(filepath)		
		self._writer = csv.DictWriter(self._file, fieldnames=['datetime', 'watts'], delimiter=';')
		if not file_exists:
			self._writer.writeheader()
		self._writer

	def _pop_rows(self):
		filepath, row = self._row_buffer.pop(0)
		rows = [row]

		while len(self._row_buffer) > 0:
			_filepath, row = self._row_buffer.pop(0)
			
			if _filepath == filepath:
				rows.append(row)
			else:
				# Add the row back to row buffer
				self._row_buffer.insert(0, row)
		return (filepath, rows)

	def write(self, _datetime, watts):
		data = {
			'datetime': _datetime.strftime('%Y-%m-%d %H:%M:%S'),
			'watts': format(watts, '.2f')
		}
	
		filepath = self._get_filepath(_datetime)
		self._row_buffer.append((filepath, data))		

		# Write to buffer
		if len(self._row_buffer) >= self.BUFFER_SIZE:
			filepath, rows = self._pop_rows()		
	
			print('Writing {} rows to file'.format(len(rows)))
			# TODO: It might be that the buffer has values from two different days, and should be split up
			file_exists = os.path.isfile(filepath)

			if not file_exists:
				os.makedirs(os.path.dirname(filepath), exist_ok=True)

			with self._open_file(filepath) as f:
				writer = csv.DictWriter(f, fieldnames=['datetime', 'watts'], delimiter=';')

				if not file_exists:
					writer.writeheader()
				writer.writerows(rows)

	def close(self):
		if self._file:
			self._file.close()


if __name__ == '__main__':
	writer = ElectricityDataWriter(DATA_STRUCTURE_BASEPATH)
	writer.write(datetime(2017, 1, 1, 2), 300)
	writer.write(datetime(2017, 1, 1, 3), 400)
	writer.write(datetime(2017, 1, 2, 1), 200)
	writer.close()

