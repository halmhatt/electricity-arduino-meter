

class TotalConsumption:
    def __init__(self, measurements: list):
        self.kilo_watt_hours = len(measurements) / 1000

    def __repr__(self):
        return 'Total consumption {:.2f}kWh'.format(self.kilo_watt_hours)