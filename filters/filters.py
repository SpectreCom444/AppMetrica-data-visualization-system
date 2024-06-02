from datetime import datetime
import config.constants as constants

class Filters:
    def __init__(self,visualization_config):
        self.filters_list =[]
        self.visualization_config =visualization_config

    def add_filter(self, filter):
        self.filters_list.append(filter)

    def event_verification(self, event):
        for filter in self.filters_list:
            if not filter(event):
                return False
        return True

    def data_filter(self,event):
        event_datetime = event.get_value(constants.EVENT_DATATIME)
        return self.visualization_config.start_date_entry <= event_datetime <= self.visualization_config.end_date_entry
