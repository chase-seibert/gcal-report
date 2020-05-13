from datetime import date, timedelta
from collections import defaultdict

import pandas as pd


def _dates_between(start, end):
    delta = end - start
    days = list()
    for i in range(delta.days):
        days.append(start + timedelta(days=i))
    return days


class GCalReport(object):

    def __init__(self, start, end):
        self._minutes_per_day = {}
        self.start = start
        self.end = end
        self._minutes_per_meeting_title = defaultdict(int)

    def add_events(self, display_name, events):
        data = defaultdict(int)
        for event in events:
            data[event['date']] += event['minutes']
        self._minutes_per_day[display_name] = dict(data)
        for event in events:
            self._minutes_per_meeting_title[event['title']] += event['minutes']

    def _get_data_frame(self):
        # see: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
        df = pd.DataFrame()
        people = list()
        for person, dates_dict in self._minutes_per_day.items():
            people.append(person)
            # fill in empty/placeholder days, sort by day
            for date in _dates_between(self.start, self.end):
                minutes = dates_dict.get(date, 0)
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

    def get_top_meetings(self, limit=10):
        top = sorted(self._minutes_per_meeting_title.items(), key=lambda x: x[1], reverse=True)
        return top[:limit]
