import csv
from datetime import datetime
import os
import sys


DATA_STRUCTURE_BASEPATH = os.path.join(os.path.dirname(__file__), 'datastructure')
CSV_FILENAME = 'watts-%Y-%m-%d-c.csv'
DB_TABLE_NAME = 'measurements'

class ElectricityDataWriter:
	# Number of rows to cache before writing to file
	BUFFER_SIZE = 5

	def __init__(self, data_structure_basepath, database_connection=None):
		self.data_structure_basepath = data_structure_basepath
		self.database_connection = database_connection
		self._file = None
		self._writer = None
		self._row_buffer = []

	def _get_filepath(self, _datetime):
		return os.path.join(self.data_structure_basepath, _datetime.strftime('%Y/%m/%Y-%m-%d'), _datetime.strftime(CSV_FILENAME))

	def _open_file(self, filepath):
		return open(filepath, 'a', newline='')

	def _add_row(self, filepath, data, index=None):
		row = (filepath, data)

		if index is not None:
			self._row_buffer.insert(index, row)
		else:
			self._row_buffer.append(row)

	def _pop_rows(self):
		"""Get all data that should be written to the same file."""
		# Get first row
		filepath, data = self._row_buffer.pop(0)
		rows = [data]

		while len(self._row_buffer) > 0:
			_filepath, data = self._row_buffer.pop(0)

			if _filepath == filepath:
				rows.append(data)
			else:
				# Add the data back to row buffer
				self._add_row(filepath=_filepath, data=data, index=0)
				break
		return (filepath, rows)

	def _add_data(self, data):
		filepath = self._get_filepath(data['datetime'])
		self._add_row(filepath=filepath, data=data)

	def _format_row(self, data):
		"""Format the data for output."""
		return {
			'datetime': data['datetime'].strftime('%Y-%m-%d %H:%M:%S'),
			'watts': format(data['watts'], '.2f')
		}

	def _store_in_database(self, _datetime, watts):
		try:
			cursor = self.database_connection.cursor()
			cursor.execute("""
				INSERT INTO `{table_name}` (measured_at, watts)
				VALUES (%s, %s);
			""".format(table_name=DB_TABLE_NAME), (_datetime, watts))
			self.database_connection.commit()
		except Exception as e:
			print('Error in database: {}'.format(e))

	def write(self, _datetime, watts):

		# Register data
		self._add_data(data={
			'datetime': _datetime,
			'watts': watts
		})

		# Upload to database
		self._store_in_database(_datetime, watts)

		# Write to buffer
		if len(self._row_buffer) >= self.BUFFER_SIZE:
			filepath, rows = self._pop_rows()

			print('Writing {} rows to file {}'.format(len(rows), filepath))
			file_exists = os.path.isfile(filepath)

			if not file_exists:
				print('Creating directories: {}'.format(os.path.dirname(filepath)))
				os.makedirs(os.path.dirname(filepath), exist_ok=True)

			with self._open_file(filepath) as f:
				print('Opening file: {}'.format(f.name))
				writer = csv.DictWriter(f, fieldnames=['datetime', 'watts'], delimiter=';')

				if not file_exists:
					writer.writeheader()

				for row in rows:
					writer.writerow(self._format_row(row))
