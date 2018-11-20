import serial
import os
import traceback
from datetime import datetime
import mysql.connector as mariadb
from electricitydatawriter import ElectricityDataWriter

DATA_STRUCTURE_BASEPATH = os.getenv('ELECTRICITY_MOUNTPOINT', '/media/electricity')
POSITIVE_EDGE = 'POSITIVE_EDGE'

DB_USER='electricity'
DB_PASSWORD='Abcdefg88'
DB_HOST_IP = '192.168.1.84'
DB_NAME = 'electricity'


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
        print('Debug: {}'.format(message))
        if not message.startswith(b'NEGATIVE_EDGE') and not message.startswith(b'POSITIVE_EDGE'):
            print('The message is broken, wait for next one')
            # Skip this message
            message = ser.readline()
            continue
        message_type, info = parse_message(message)
        timestamp = info['Milliseconds']

        if message_type == POSITIVE_EDGE and isinstance(timestamp, int):
            # print(info)

            if prev_timestamp:
                watts = calculate_watts(timestamp, prev_timestamp)
                data_writer.write(_datetime=datetime.utcnow(),
                                  watts=watts)
                print('{}: {:.2f} Watts (arduino timestamp: {timestamp} ms)'.format(datetime.now(), watts, timestamp=timestamp))

            prev_timestamp = timestamp

        message = ser.readline()

def connect_db():
    mariadb_connection = mariadb.connect(host=DB_HOST_IP,
                                         user=DB_USER,
                                         password=DB_PASSWORD,
                                         database=DB_NAME)
    return mariadb_connection

try:
    ser = serial.Serial('/dev/ttyUSB0')

    # Setup database
    db_connection = connect_db()

    # Skip first message, if any in the buffer
    ser.flush()

    data_writer = ElectricityDataWriter(DATA_STRUCTURE_BASEPATH,
                                        database_connection=db_connection)

    read_from_serial(ser, data_writer)

    db_connection.close()
except Exception as e:
    print('Error: {}'.format(e))
    print(traceback.format_exc())
    with open('error.log', 'w') as f:
        f.write('Error: {}'.format(e))
        f.write(traceback.format_exc())
