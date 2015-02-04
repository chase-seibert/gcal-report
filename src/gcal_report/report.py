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

    def _get_data_frame(self):
        df = pd.DataFrame()
        people = list()
        for person, dates_dict in self._minutes_per_day.items():
            people.append(person)
            for date, minutes in dates_dict.items():
                df.at[date, person] = minutes
        # create summary column, sum of other columns
        df['summary'] = df.mean(axis=1)
        return df

    def dump(self):
        return self._get_data_frame()

    def summary(self):
        df = self._get_data_frame()
        return df.describe()

    def csv(self, output_file):
        df = self._get_data_frame()
        df.to_csv(output_file)

