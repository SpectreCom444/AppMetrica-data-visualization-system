from datetime import datetime
import constants
class VisualizationParams:
    def __init__(self):
        self.time_limits= False
        self.type_data=constants.EVENTS

    def set_data_to_display(self, type_of_data, fig_canvas, selected_data,selected_chart_type,other_reference ):
        self.type_of_data=type_of_data
        self.canvas=fig_canvas
        self.selected_data=selected_data
        self.selected_chart_type=selected_chart_type   
        self.other_reference=other_reference
        

    def set_data_time(self, start_date_entry, end_date_entry):
        if isinstance(start_date_entry, str) and len(start_date_entry) == 10:
            start_date_entry += ' 00:00:00'
        if isinstance(end_date_entry, str) and len(end_date_entry) == 10:
            end_date_entry += ' 23:59:59'

        self.start_date_entry = start_date_entry
        self.end_date_entry = end_date_entry
    
    def set_type_data(self, type_data):
        self.type_data=type_data

    def get_time_limits(self):
        return self.time_limits

