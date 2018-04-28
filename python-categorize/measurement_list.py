import csv

from measurement import Measurement


class MeasurementList:
    def __init__(self, filepath):
        self.filepath = filepath

    def get_measurements(self) -> list:
        measurements = []

        with open(self.filepath, newline='') as f:
            reader = csv.DictReader(f, delimiter=';')
            return [Measurement(index, row) for index, row in enumerate(reader)]