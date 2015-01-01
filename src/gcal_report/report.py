from collections import defaultdict


class GCalReport(object):

    def __init__(self):
        self._minutes_per_day = {}

    def add_events(self, display_name, events):
        data = defaultdict(int)
        for event in events:
            data[event['date']] += event['minutes']
        self._minutes_per_day[display_name] = dict(data)

    def summary(self):
        return self._minutes_per_day

