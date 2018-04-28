from datetime import timedelta

from categorizers.base_math import BaseMath
from measurement import Measurement


class BaseStep(BaseMath):
    def __init__(self, measurements):
        self.measurements = measurements

    @property
    def first(self) -> Measurement:
        """First measurement of step."""
        return self.measurements[0]

    @property
    def middle(self) -> Measurement:
        return self.measurements[2]

    @property
    def last(self) -> Measurement:
        """Last measurement of step."""
        return self.measurements[-1]

    @property
    def diff(self) -> float:
        """Difference is watts."""
        return self.last.watts - self.first.watts

    @property
    def duration(self) -> timedelta:
        return self.last.utc_datetime - self.first.utc_datetime

    @property
    def kilowatt_hours(self) -> float:
        return len(self.measurements) / 1000
