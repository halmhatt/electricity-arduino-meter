from categorizers.base_step import BaseStep
from measurement import Measurement


class PositiveStep(BaseStep):
    MIN_WATT_DIFF = 40

    @property
    def has_bottom(self):
        return self.similar([m.watts for m in self.measurements[:2]])

    @property
    def has_top(self):
        return self.similar([m.watts for m in self.measurements[-2:]])

    @classmethod
    def find_all(cls, input_measurements: list) -> list:
        steps = []
        m = input_measurements
        for measurements in zip(m, m[1:], m[2:], m[3:], m[4:]):
            step = cls(measurements)

            if step.has_bottom and step.has_top and step.diff > cls.MIN_WATT_DIFF:
                steps.append(step)
        return steps

    def __repr__(self):
        return 'Positive step {:%H:%M:%S}: {:.0f}W {:+.0f}W'.format(
            self.middle.local_datetime,
            self.first.watts,
            self.diff)
