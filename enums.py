from enum import Enum


class SplitTimeMode(Enum):
    NOSPLIT = "No split"
    SPLITBYDAY = "Split by day"
    SPLITBYHOURS = "Split by hours"


class HistogramType(Enum):
    STACKET = "Stacket"
    CLUSTERED = "Clustered"


class Orientation(Enum):
    VERTICAL = "Vertical"
    HORIZONTAL = "Horizontal"


class TypeOfMeasurement(Enum):
    PERCENTED = "Percented"
    UNITED = "United"


class DateType(Enum):
    EVENTS = "Events"
    SESSIONS = "Sessions"
    USERS = "Users"


class GraphType(Enum):
    LINE = 'Line'
    PIE = 'Pie'
    RING = 'Ring'
    SCATTER = 'Scatter'
    HISTOGRAM = 'Histogram'
    BUBBLE = 'Bubble'
    AREA = 'Area'
    FUNNEL = 'Funnel'
