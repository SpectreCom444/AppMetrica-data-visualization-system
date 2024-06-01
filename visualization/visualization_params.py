from datetime import datetime
import config.constants as constants
from enums.enums import DisplayMode,HistogramType,Orientation,GraphType,TypeOfMeasurement
class VisualizationParams:
    def __init__(self):
        self.time_limits= False
        self.type_data=constants.EVENTS
        self.type_of_measurement =TypeOfMeasurement.UNITS
        self.selected_chart_type= GraphType.LINE
        self.display_mode = DisplayMode.TOTAL
        self.histogram_type = HistogramType.SUMMATION
        self.orientation = Orientation.HORIZONTAL

    def set_chart_type(self, chart_type):
        self.chart_type=chart_type

    def set_display_mode(self,display_mode):
        self.display_mode=display_mode
    
    def set_histogram_type(self,histogram_type):
        self.histogram_type=histogram_type

    def set_type_of_measurement(self,type_of_measurement):
        self.type_of_measurement=type_of_measurement

    def set_orientation(self,orientation):
        self.orientation=orientation

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

