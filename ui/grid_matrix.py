from typing import List, Optional
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QDesktopWidget
from ui.matplotlib_canvas import MatplotlibCanvas


class GridMatrix:
    def __init__(self, workspace_window: QMainWindow, size_x: int = 1, size_y: int = 1):
        self._size_x: int = size_x
        self._size_y: int = size_y
        self._workspace_window: QMainWindow = workspace_window
        self._matrix: List[List[MatplotlibCanvas]] = [
            [self._create_canvas(0, 0)]]
        self.selected_canvas: MatplotlibCanvas = self.get_canvas(0, 0)
        self.clipboard_visualization_config: Optional[dict] = None

    def update_matrix_size(self, size_x: int, size_y: int) -> None:
        self._resize_matrix_rows(size_x)
        self._resize_matrix_columns(size_y)
        self._size_x = size_x
        self._size_y = size_y

    def _resize_matrix_rows(self, size_x: int) -> None:
        if self._size_x < size_x:
            for x in range(self._size_x, size_x):
                self._matrix.append([self._create_canvas(x, y)
                                    for y in range(self._size_y)])
        elif self._size_x > size_x:
            for x in range(size_x, self._size_x):
                for y in range(self._size_y):
                    self._remove_canvas(x, y)
            self._matrix = self._matrix[:size_x]

    def _resize_matrix_columns(self, size_y: int) -> None:
        if self._size_y < size_y:
            for x in range(len(self._matrix)):
                for y in range(self._size_y, size_y):
                    self._matrix[x].append(self._create_canvas(x, y))
        elif self._size_y > size_y:
            for x in range(len(self._matrix)):
                for y in range(size_y, self._size_y):
                    self._remove_canvas(x, y)
                self._matrix[x] = self._matrix[x][:size_y]

    def _create_canvas(self, pos_x: int, pos_y: int) -> MatplotlibCanvas:
        canvas_container = QWidget()
        layout = QVBoxLayout(canvas_container)
        canvas_container.setLayout(layout)
        canvas = MatplotlibCanvas(
            canvas_container, self.set_selected_canvas, pos_x, pos_y)
        layout.addWidget(canvas)

        self._configure_canvas_container_size(canvas_container)
        self._workspace_window.gridt_GS.addWidget(
            canvas_container, pos_x, pos_y)
        return canvas

    def _configure_canvas_container_size(self, canvas_container: QWidget) -> None:
        screen = QDesktopWidget().screenGeometry()
        min_width = screen.width() // 4
        min_height = screen.height() // 3
        max_width = screen.width()
        max_height = screen.height()
        canvas_container.setMinimumSize(min_width, min_height)
        canvas_container.setMaximumSize(max_width, max_height)

    def _remove_canvas(self, pos_x: int, pos_y: int) -> None:
        canvas_container = self._workspace_window.gridt_GS.itemAtPosition(
            pos_x, pos_y).widget()
        self._workspace_window.gridt_GS.removeWidget(canvas_container)
        canvas_container.deleteLater()

    def plot_canvas(self) -> None:
        self.clear_selected_canvas()
        self._workspace_window.data_for_chart()
        self._workspace_window.update_tools()

    def remove_all(self) -> None:
        for x in range(self._size_x):
            for y in range(self._size_y):
                self._remove_canvas(x, y)
        self._reset_matrix()
        self._workspace_window.update_tools()

    def _reset_matrix(self) -> None:
        self._matrix = [[self._create_canvas(0, 0)]]
        self.selected_canvas = self.get_canvas(0, 0)
        self._size_x = 1
        self._size_y = 1
        self._workspace_window.size_x_combobox.setCurrentIndex(0)
        self._workspace_window.size_y_combobox.setCurrentIndex(0)

    def get_canvas(self, pos_x: int, pos_y: int) -> MatplotlibCanvas:
        return self._matrix[pos_x][pos_y]

    def set_selected_canvas(self, canvas: MatplotlibCanvas) -> None:
        self.selected_canvas = canvas
        self._workspace_window.update_tools()

    def clear_selected_canvas(self) -> None:
        pos_x, pos_y = self.selected_canvas.get_position()
        self._remove_canvas(pos_x, pos_y)
        self._matrix[pos_x][pos_y] = self._create_canvas(pos_x, pos_y)
        self.selected_canvas = self._matrix[pos_x][pos_y]
        self._workspace_window.update_tools()

    def clear_all_canvases(self) -> None:
        for x, row in enumerate(self._matrix):
            for y, _ in enumerate(row):
                self._remove_canvas(x, y)
                self._matrix[x][y] = self._create_canvas(x, y)
        self._workspace_window.update_tools()

    def copy_canvas(self) -> None:
        self.clipboard_visualization_config = self.selected_canvas.get_visualization_parameters()
        self._workspace_window.update_tools()

    def paste_canvas(self) -> None:
        self.clear_selected_canvas()
        if self.clipboard_visualization_config:
            self.selected_canvas.set_visualization_parameters(
                self.clipboard_visualization_config)
            self.selected_canvas.visualization_config.canvas = self.selected_canvas
            self._workspace_window.data_visualizer.plot_copy_chart(
                self.selected_canvas.visualization_config, self._workspace_window.loading
            )
        self._workspace_window.update_tools()

    def cut_canvas(self) -> None:
        self.copy_canvas()
        self.clear_selected_canvas()
        self._workspace_window.update_tools()
