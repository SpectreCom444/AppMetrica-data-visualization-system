from enums import GraphType
from config.constants import SPLIT_TIME_MODE, TYPE_OF_MEASUREMENT, HISTOGRAM_TYPE, ORIENTATION

graph_parameters = {
    GraphType.LINE: [SPLIT_TIME_MODE, TYPE_OF_MEASUREMENT],
    GraphType.PIE: [],
    GraphType.RING: [],
    GraphType.SCATTER: [SPLIT_TIME_MODE, TYPE_OF_MEASUREMENT],
    GraphType.HISTOGRAM: [SPLIT_TIME_MODE, HISTOGRAM_TYPE, ORIENTATION, TYPE_OF_MEASUREMENT],
    GraphType.BUBBLE: [TYPE_OF_MEASUREMENT],
    GraphType.AREA: [SPLIT_TIME_MODE, TYPE_OF_MEASUREMENT],
    GraphType.FUNNEL: [TYPE_OF_MEASUREMENT],
}
