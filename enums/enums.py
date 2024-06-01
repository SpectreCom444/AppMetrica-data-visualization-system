from enum import Enum

class DisplayMode(Enum):
    TOTAL = 1
    DAY = 2
    HOURSE = 3

class HistogramType(Enum):
    SUMMATION = 1
    COMPARISON = 2

class Orientation(Enum):   
    HORIZONTAL = 1
    VERTICAL = 2

class TypeOfData(Enum):
    FIELD_NAME = 1
    TREE = 2

class TypeOfMeasurement(Enum):
    UNITS = 1
    PERCENTAGES = 2

class GraphType(Enum):
    LINE = 'line'
    BAR = 'bar'
    PIE = 'pie'
    RING = 'ring'
    SCATTER = 'scatter'
    HISTOGRAM = 'histogram'
    BUBBLE = 'bubble'
    AREA = 'area'
    FUNNEL = 'funnel'