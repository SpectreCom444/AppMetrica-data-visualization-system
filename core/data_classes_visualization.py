import config.constants as constants
from enums import SplitTimeMode, HistogramType, Orientation, GraphType, TypeOfMeasurement
from PyQt5.QtCore import QDate
from dataclasses import dataclass, field, fields


# @dataclass
class VisualizationConfig:
    def __init__(self):
        self.type_data = constants.EVENTS
        self.type_of_measurement = TypeOfMeasurement.UNITED
        self.selected_chart_type = GraphType.LINE
        self.display_mode = SplitTimeMode.NOSPLIT
        self.histogram_type = HistogramType.STACKET
        self.orientation = Orientation.HORIZONTAL
        self.start_date_entry = QDate.currentDate()
        self.end_date_entry = QDate.currentDate()
        self.other_reference = 0
        self.selected_data = ""
        self.canvas = None

    def copy(self, reference):
        self.type_data = reference.type_data
        self.type_of_measurement = reference.type_of_measurement
        self.selected_chart_type = reference.selected_chart_type
        self.display_mode = reference.display_mode
        self.histogram_type = reference.histogram_type
        self.orientation = reference.orientation
        self.start_date_entry = reference.start_date_entry
        self.end_date_entry = reference.end_date_entry
        self.other_reference = reference.other_reference
        self.selected_data = reference.selected_data
        self.canvas = reference.canvas
