from config.constants import EVENT_DATETIME


class Filters:

    def event_verification(self, event, filters_list):
        for filter in filters_list:
            if not filter.check(event):
                return False
        return True


class DateFilter():
    def __init__(self, start_date_entry, end_date_entry):
        self.start_date_entry = start_date_entry
        self.end_date_entry = end_date_entry

    def check(self, event):
        event_datetime = event.get_value(EVENT_DATETIME)
        return self.start_date_entry <= event_datetime <= self.end_date_entry


class EventFilter():
    def __init__(self,  invert, selected_options):
        self.invert = invert
        self.selected_options = selected_options

    def check(self, event):
        def check_event(tree, metric_names):
            if metric_names[0] in tree:
                if len(metric_names) > 1:
                    return check_event(tree[metric_names[0]], metric_names[1:])
                else:
                    if isinstance(tree, dict):
                        return True
                    else:
                        return None
            else:
                return None
        if len(self.selected_options) == 0:
            return True
        if not self.invert:
            return check_event(event.data, self.selected_options)
        else:
            return not check_event(event.data, self.selected_options)
