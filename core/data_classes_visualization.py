from enums import SplitTimeMode, HistogramType, Orientation, GraphType, TypeOfMeasurement, DateType
from PyQt5.QtCore import QDate
from dataclasses import dataclass, field
from typing import List, Any


@dataclass
class VisualizationConfig:
    type_data: DateType = DateType.EVENTS
    type_of_measurement: TypeOfMeasurement = TypeOfMeasurement.UNITED
    selected_chart_type: GraphType = GraphType.LINE
    display_mode: SplitTimeMode = SplitTimeMode.NOSPLIT
    histogram_type: HistogramType = HistogramType.STACKET
    orientation: Orientation = Orientation.HORIZONTAL
    start_date_entry: QDate = field(default_factory=QDate.currentDate)
    end_date_entry: QDate = field(default_factory=QDate.currentDate)
    other_reference: int = 0
    selected_data: str = ""
    canvas: Any = None
    filters_list: List[Any] = field(default_factory=list)

    def copy(self, reference: 'VisualizationConfig') -> None:
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
        self.filters_list = reference.filters_list[:]
