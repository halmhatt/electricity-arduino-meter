import time
from datetime import datetime


class Measurement:
    def __init__(self, index, data: dict):
        self.index = index
        self.watts = float(data['watts'])
        self.utc_datetime = datetime.strptime(data['datetime'], '%Y-%m-%d %H:%M:%S')

    @property
    def local_datetime(self):
        """Convert timestamp in UTC to local timestamp."""
        now_timestamp = time.time()
        offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
        return self.utc_datetime + offset
