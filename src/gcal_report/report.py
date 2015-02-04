from collections import defaultdict
import pandas as pd


class GCalReport(object):

    def __init__(self):
        self._minutes_per_day = {}

    def add_events(self, display_name, events):
        data = defaultdict(int)
        for event in events:
            data[event['date']] += event['minutes']
        self._minutes_per_day[display_name] = dict(data)

    def get_data_frame(self):
        sum_minutes_per_day = defaultdict(int)
        for person, dates_dict in self._minutes_per_day.items():
            for date, minutes in dates_dict.items():
                sum_minutes_per_day[date] += minutes
        num_people = len(self._minutes_per_day.keys())
        return pd.DataFrame({
            'date': sum_minutes_per_day.keys(),
            # must be a better way to do this
            'meeting_min': [minutes / num_people for minutes in sum_minutes_per_day.values()],
            'meeting_hours': [minutes / num_people / 60.0 for minutes in sum_minutes_per_day.values()],
        })

    def dump(self):
        return self.get_data_frame()

    def summary(self):
        df = self.get_data_frame()
        return df.describe()

