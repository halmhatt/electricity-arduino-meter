import logging

from categorizers.negative_step import NegativeStep
from categorizers.positive_step import PositiveStep
from categorizers.total_consumption import TotalConsumption
from measurement_list import MeasurementList
from overlap_filter import OverlapFilter
from test.categorizers.boiling_water import BoilingWater

logging.basicConfig(level='DEBUG')


FILEPATH = '/Users/jacob/Documents/offline_electricity/2018/04/2018-04-26/watts-2018-04-26-c.csv'
measurement_list = MeasurementList(FILEPATH)

measurements = measurement_list.get_measurements()

# Categorize steps
positive_steps = PositiveStep.find_all(measurements)
positive_steps = OverlapFilter.filter(positive_steps)
# for step in positive_steps:
#     print(step)

negative_steps = NegativeStep.find_all(measurements)
negative_steps = OverlapFilter.filter(negative_steps)
# for step in negative_steps:
#     print(step)

all_steps = sorted(positive_steps + negative_steps, key=lambda m: m.first.utc_datetime)
# print(all_steps)

print()
# Find water boiler
boiling_water = BoilingWater.find_all(all_steps, measurements)
for b in boiling_water:
    print(b)
    # print([m.watts for m in b.measurements])

print(TotalConsumption(measurements))

# for measurement in measurements:
#     print('{}: {}W'.format(measurement.local_datetime, measurement.watts))