import logging

from categorizers.base_step import BaseStep
from categorizers.negative_step import NegativeStep
from categorizers.positive_step import PositiveStep

logger = logging.getLogger(__name__)


class BoilingWater(BaseStep):
    WATT_DIFF = 2000

    def __init__(self, measurements: list, positive_step: PositiveStep, negative_step: NegativeStep):
        super().__init__(measurements)
        self.positive_step = positive_step
        self.negative_step = negative_step

    @classmethod
    def find_all(cls, sorted_steps: list, measurements: list) -> list:
        """Find all boiling water.
        :param sorted_steps List of positive and negative steps, sorted on date.
        """
        boiling_steps = []
        positive_step = None
        negative_step = None
        for step in sorted_steps:
            if isinstance(step, PositiveStep) and cls.similar([step.diff, cls.WATT_DIFF]):
                positive_step = step
                logger.debug('Found positive step {}'.format(positive_step))

            if positive_step and isinstance(step, NegativeStep) and cls.similar([step.diff, -cls.WATT_DIFF]):
                negative_step = step
                logger.debug('Found negative step {}'.format(negative_step))

            if positive_step and negative_step:
                boiling_steps.append(BoilingWater(measurements[positive_step.first.index:negative_step.last.index],
                                                  positive_step=positive_step,
                                                  negative_step=negative_step))
                positive_step = None
                negative_step = None
        return boiling_steps

    @property
    def mean_watts(self):
        """An estimate of how much watts this step is using on average."""
        return (self.positive_step.diff - self.negative_step.diff) / 2

    @property
    def estimated_kilowatt_hours(self):
        logger.debug('Mean watts: {:.2f}W'.format(self.mean_watts))
        return self.mean_watts * self.duration.total_seconds() / 3600 / 1000

    def __repr__(self):
        return 'Boiling water {start_datetime:%H:%M:%S} ({duration}) ~{kilowatt_hours:.3f}kWh'.format(
            start_datetime=self.first.local_datetime,
            duration=self.duration,
            kilowatt_hours=self.estimated_kilowatt_hours)
