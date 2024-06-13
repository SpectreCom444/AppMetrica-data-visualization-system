from core.data_classes_visualization import VisualizationConfig
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QSizePolicy, QWidget
from typing import Callable, Tuple
import matplotlib.pyplot as plt


class MatplotlibCanvas(FigureCanvasQTAgg):
    def __init__(self, parent: QWidget, on_click_callback: Callable[['MatplotlibCanvas'], None], pos_x: int, pos_y: int) -> None:
        self.fig: Figure = Figure()
        super().__init__(self.fig)
        self.setParent(parent)
        self._on_click_callback: Callable[[
            'MatplotlibCanvas'], None] = on_click_callback
        self.mpl_connect("button_press_event", self._on_click)
        self.visualization_config: VisualizationConfig = VisualizationConfig()
        self._pos_x: int = pos_x
        self._pos_y: int = pos_y
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()
        self.ax: Optional[plt.Axes] = None

    def create_axes(self) -> None:
        if self.ax is None:
            self.ax = self.fig.add_subplot(111)
            self.ax.grid(True)

    def set_visualization_parameters(self, visualization_config: VisualizationConfig) -> None:
        self.visualization_config.copy(visualization_config)
        self.updateGeometry()

    def get_visualization_parameters(self) -> VisualizationConfig:
        return self.visualization_config

    def get_position(self) -> Tuple[int, int]:
        return self._pos_x, self._pos_y

    def _on_click(self, event) -> None:
        self._on_click_callback(self)
