from config.visualization_config import VisualizationConfig
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

class MatplotlibCanvas(FigureCanvasQTAgg):
    def __init__(self, parent, on_click_callback,pos_x,pos_y):
        self.fig = Figure()
        super(MatplotlibCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.on_click_callback = on_click_callback
        self.mpl_connect("button_press_event", self.on_click)
        self.visualization_config = VisualizationConfig()
        self.pos_x=pos_x
        self.pos_y = pos_y

    def set_visualization_parameters(self,visualization_config):
        self.visualization_config.copy(visualization_config)
    
    def get_visualization_parameters(self):
        return self.visualization_config

    def get_position(self):
        return (self.pos_x,self.pos_y)
    
    def on_click(self, event):
        print(self.pos_x, self.pos_y)
        self.on_click_callback(self)
    