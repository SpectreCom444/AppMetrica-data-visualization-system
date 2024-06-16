from enums import SplitTimeMode, HistogramType, Orientation, GraphType, TypeOfMeasurement, DateType
from PyQt5.QtCore import QDate
from dataclasses import dataclass, field
from typing import List, Any


@dataclass
class VisualizationConfig:
    type_data: DateType = DateType.EVENTS
    type_of_measurement: TypeOfMeasurement = TypeOfMeasurement.PERCENTED
    chart_type: GraphType = GraphType.LINE
    split_time_mode: SplitTimeMode = SplitTimeMode.NOSPLIT
    histogram_type: HistogramType = HistogramType.STACKET
    orientation: Orientation = Orientation.VERTICAL
    start_date_entry: QDate = field(default_factory=QDate.currentDate)
    end_date_entry: QDate = field(default_factory=QDate.currentDate)
    treshold: int = 0
    selected_options: str = ""
    canvas: Any = None
    filters_list: List[Any] = field(default_factory=list)

    def copy(self, reference: 'VisualizationConfig') -> None:
        self.type_data = reference.type_data
        self.type_of_measurement = reference.type_of_measurement
        self.chart_type = reference.chart_type
        self.split_time_mode = reference.split_time_mode
        self.histogram_type = reference.histogram_type
        self.orientation = reference.orientation
        self.start_date_entry = reference.start_date_entry
        self.end_date_entry = reference.end_date_entry
        self.treshold = reference.treshold
        self.selected_options = reference.selected_options[:]
        self.canvas = reference.canvas
        self.filters_list = reference.filters_list[:]
