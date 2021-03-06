import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
from datetime import datetime, timezone
import time
import sys
import os


def datetime_from_utc_to_local(utc_datetime):
    """Convert timestamp in UTC to local timestamp."""
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

def read_file(filepath):
    """Read CSV filepath and return parsed values."""
    watts_list = []
    datetime_list = []
    total_watt_hours = 0

    with open(filepath, newline='') as f:
        reader = csv.DictReader(f, delimiter=';')

        for row in reader:
            _datetime = datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S')
            _datetime = datetime_from_utc_to_local(_datetime)
            watts = float(row['watts'])
            datetime_list.append(_datetime)
            watts_list.append(watts)
            total_watt_hours += 1
    print('Total consumption: {:.2f} kWh'.format(total_watt_hours / 1000))
    return (datetime_list, watts_list)

def moving_average(data, num_points=3):
    new_data = []

    for i, value in enumerate(data[:-num_points]):
        new_data.append(sum(data[i:i+num_points]) / num_points)
    return new_data



def show_plot(datetime_list, watts_list):
    """Show a plot of the data."""
    # Configure dates on X-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    plt.plot(datetime_list, watts_list, 'b-x')
    # plt.plot(datetime_list[:-5], moving_average(watts_list, 5), color='red')
    plt.ylabel('Watts')
    plt.xlabel('Local time')
    plt.title('Measurements between {} and {}'.format(datetime_list[0].strftime('%Y-%m-%d %H:%M:%S'),
                                                      datetime_list[-1].strftime('%Y-%m-%d %H:%M:%S')))
    plt.show()

if __name__ == '__main__':
    filepath = sys.argv[1]

    if os.path.isfile(filepath):
        datetime_list, watts_list = read_file(filepath)
        show_plot(datetime_list, watts_list)
