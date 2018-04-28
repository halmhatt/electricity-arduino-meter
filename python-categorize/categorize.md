

# Input <csv-file>
# Create visitors that take a window of x measurements as input. Or it should get the entire list and work on it.


### Helper functions

## Positive step
# From one "constant" value (e.g. 2 measurements that are quite the same) up to a "constant" value

## Negative step
# Same as positive step but the inverse

## Contant
# A "constant" value, with very small differences in watts (should it be in %, e.g. changes only 5% between measurements)
# Should have a minimum length of e.g. 3 measurements
# Should have:
#  * length
#  * start
#  * stop
#  * difference in measurements
#  * mean
#  * max
#  * min 
#  * total_watts


### Higher order functions

## Wake up:
# Workdays between 05-08 and weekends between 06-10 swedish time
# Electricity should absolutely go up with a lot, like from ~300W to ~2000W

## Go to sleep
# Electricity should start to go down
# Should be about 22 swedish time
# The last part should be the lights should go off

## Philips hue lights off
# All on

## Water boiler
# +800W constantly for about 3-5 minutes
# Usually in the morning

## Microwave
# +800W constantly for about 0.5-5 minutes

## Charge phone
# From about 22 Swedish time
# Some watts, i dont know

## Television is on
# ...

## Lights in the hall
# On and off
