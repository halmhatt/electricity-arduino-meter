import serial
import os
from datetime import datetime
from electricitydatawriter import ElectricityDataWriter

DATA_STRUCTURE_BASEPATH = '/media/electricity'
POSITIVE_EDGE = 'POSITIVE_EDGE'


def parse_message(message: str):
	message_parts = message.decode('ascii').strip('\n\r').split('::')
	message_type = message_parts[0]
	parts= message_parts[1].split(', ')
	info = dict()
	
	for part in parts:
		subparts = part.split(': ')
		key = subparts[0]
		value = subparts[1]		

		if value.isnumeric():
			value = int(subparts[1])	
	
		info[key] = value
	return (message_type, info)	


def calculate_watts(timestamp: int, prev_timestamp: int):	
	diff = timestamp - prev_timestamp
	return 1.0 / (diff / 60 / 60 / 1000)	


def read_from_serial(ser, data_writer):
	# Previous timestamp
	prev_timestamp = None
	message = ser.readline()
	while message:
		message_type, info = parse_message(message)
		timestamp = info['Milliseconds']		

		if message_type == POSITIVE_EDGE and isinstance(timestamp, int):
			# print(info)

			if prev_timestamp:
				watts = calculate_watts(timestamp, prev_timestamp)
				data_writer.write(datetime.utcnow(), watts)
				print('{}: {:.2f} Watts'.format(datetime.now(), watts))

			prev_timestamp = timestamp

		message = ser.readline()

try:
	ser = serial.Serial('/dev/ttyUSB0')
	ser.open()
	
	# Skip first message, if any in the buffer
	ser.flush()
	
	data_writer = ElectricityDataWriter(DATA_STRUCTURE_BASEPATH)

	read_from_serial(ser, data_writer)
except KeyboardInterrupt:
	data_writer.close()
	print('Closing file pointer')

