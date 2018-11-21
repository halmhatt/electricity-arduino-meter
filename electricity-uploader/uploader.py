import csv
import glob
import os

import datetime
import mysql.connector as mariadb

DB_USER='electricity'
DB_PASSWORD='Abcdefg88'
DB_TABLE_NAME = 'measurements'


def connect():
    mariadb_connection = mariadb.connect(host='192.168.1.84',
                                         user=DB_USER,
                                         password=DB_PASSWORD,
                                         database='electricity')
    return mariadb_connection


def setup_db(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `{table_name}` (
            `id` INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
            `measured_at` DATETIME NOT NULL,
            `watts` DECIMAL(7, 2) UNSIGNED NOT NULL,
            PRIMARY KEY (`id`),
            INDEX `measured_at_idx` (`measured_at`)
        ) CHARACTER SET utf8;
        """.format(table_name=DB_TABLE_NAME))
        connection.commit()

        for result in cursor:
            print(result)

    except mariadb.Error as error:
        print('Error: {}'.format(error))


def _parse_row(row: dict):
    parsed_datetime = datetime.datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S')
    return (parsed_datetime, float(row['watts']))


def upload_file(connection, filepath):
    cursor = connection.cursor()

    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        try:
            cursor.executemany("""
            INSERT INTO `{table_name}` (measured_at, watts)
            VALUES (%s, %s);
            """.format(table_name=DB_TABLE_NAME), (_parse_row(row) for row in reader))
        except mariadb.Error as error:
            print('Error: {}'.format(error))

    connection.commit()


def find_all_files(base_dir):
    filepaths = glob.glob('{base_dir}/*/*/*-c.csv'.format(base_dir=base_dir))
    return sorted(filepaths)


if __name__ == '__main__':
    connection = connect()
    setup_db(connection)
    for filepath in find_all_files('/Volumes/electricity/2018'):
        print('Uploading {}'.format(filepath))
        upload_file(connection, filepath)
    # upload_file(connection, os.path.join(os.path.dirname(__file__), 'watts-2018-11-17-c.csv'))
    connection.close()
