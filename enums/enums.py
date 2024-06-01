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