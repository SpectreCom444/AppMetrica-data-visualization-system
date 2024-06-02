from core.shared import shared_state
from enums.enums import TypeOfData
from filters.filters import Filters
import config.constants as constants
from visualization.plotter import Plotter


class DataVisualizer:

    def __init__(self):
        self.plotter = None

    def counter(self,elements, metric_name, visualization_params, filters):
        count = {}
        if visualization_params.type_data == constants.EVENTS:
            self.counter_events(elements, metric_name, visualization_params, count, filters)
        elif visualization_params.type_data == constants.SESSIONS:
            self.counter_sessions(elements, metric_name, visualization_params, count, filters)
        elif visualization_params.type_data == constants.USERS:
            self.counter_users(elements, metric_name, visualization_params, count, filters)
        return count


    def counter_sessions(self,elements, metric_name, visualization_params, count, filters):
        for sessions in elements:
            sessions_count = {}
            self.counter_events(sessions.get_events(), metric_name, visualization_params, sessions_count, filters)
            for key in sessions_count.keys():
                if key in count:
                    count[key] += 1
                else:
                    count[key] = 1


    def counter_users(self,elements, metric_name, visualization_params, count, filters):
        for user in elements:
            user_count = {}
            self.counter_sessions(user.get_sessions(), metric_name, visualization_params, user_count, filters)
            for key in user_count.keys():
                if key in count:
                    count[key] += 1
                else:
                    count[key] = 1


    def counter_events(self,elements, metric_name, visualization_params, count, filters):
        for event in elements:
            if filters.event_verification(event):
                if TypeOfData.FIELD_NAME == visualization_params.type_of_data:
                    value = event.get_value(metric_name)
                    if value in count:
                        count[value] += 1
                    else:
                        count[value] = 1
                elif TypeOfData.TREE == visualization_params.type_of_data:
                    value = self.counter_events_list(event, metric_name)
                    if isinstance(value, str):
                        if value in count:
                            count[value] += 1
                        else:
                            count[value] = 1
                    else:
                        for name in value:
                            if name in count:
                                count[name] += 1
                            else:
                                count[name] = 1
        return count

    @classmethod
    def counter_events_list(cls,event, metric_names):

        def check_event(tree, metric_names):
            if metric_names[0] in tree:
                if len(metric_names) > 1:
                    return check_event(tree[metric_names[0]], metric_names[1:])
                else:
                    if isinstance(tree, dict):
                        return tree[metric_names[0]]
                    else:
                        return None
            else:
                return None

        events_count = {}
        names = check_event(event.__dict__[constants.EVENT_JSON], metric_names)
        if names is not None:
            return names

        return events_count

    @classmethod
    def counting_other(cls, data, other_threshold):
        total = sum(data.values())
        other_sum = 0

        keys_to_remove = [key for key, value in data.items() if (value / total) * 100 < other_threshold]

        for key in keys_to_remove:
            other_sum += data.pop(key)

        if other_sum > 0:
            if 'other' in data:
                data['other'] += other_sum
            else:
                data['other'] = other_sum

        return data

    def create_new_plotter(self,visualization_params):
        self.plotter = Plotter(visualization_params.canvas, visualization_params.selected_data, visualization_params.type_of_measurement,visualization_params.orientation)

    def add_chart(self, visualization_params):
        if visualization_params.type_data == constants.EVENTS:
            data = shared_state.events_result
        elif visualization_params.type_data == constants.SESSIONS:
            data = shared_state.sessions_result
        elif visualization_params.type_data == constants.USERS:
            data = shared_state.users_result

        filters = Filters(visualization_params)

        if visualization_params.get_time_limits:
            filters.add_filter(filters.data_filter)

        events_count = self.counter(data, visualization_params.selected_data, visualization_params, filters)

        events_count = self.counting_other(events_count, visualization_params.other_reference) 
        self.plotter.plot(visualization_params.selected_chart_type, events_count)
    




