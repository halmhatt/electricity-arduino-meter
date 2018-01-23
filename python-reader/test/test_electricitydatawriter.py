from unittest import TestCase
from electricitydatawriter import ElectricityDataWriter
import datetime


class TestElectricityDataWriter(TestCase):

    def setUp(self):
        self.writer = ElectricityDataWriter('/basepath')

    def test__get_filepath(self):
        _datetime = datetime.datetime(2017, 1, 1)
        path = self.writer._get_filepath(_datetime)
        self.assertEqual(path, '/basepath/2017/01/2017-01-01/watts-2017-01-01-c.csv')

    def test___pop_rows(self):
        # Setup
        fp1 = '/basepath/2017/01/2017-01-01/watts-2017-01-01-c.csv'
        fp2 = '/basepath/2017/01/2017-01-02/watts-2017-01-02-c.csv'
        d1 = {'datetime': '2017-01-01 13:00:00', 'watts': 1.00}
        d2 = {'datetime': '2017-01-01 23:00:00', 'watts': 2.00}
        d3 = {'datetime': '2017-01-02 01:00:00', 'watts': 3.00}
        self.writer._add_row(filepath=fp1, data=d1)
        self.writer._add_row(filepath=fp1, data=d2)
        self.writer._add_row(filepath=fp2, data=d3)

        filepath, rows = self.writer._pop_rows()
        self.assertEqual(filepath, '/basepath/2017/01/2017-01-01/watts-2017-01-01-c.csv')
        self.assertEqual(rows, [d1, d2])
        self.assertEqual(self.writer._row_buffer, [(fp2, d3)])
