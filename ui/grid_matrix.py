from PyQt5.QtWidgets import QMainWindow, QApplication, QCheckBox, QPushButton, QVBoxLayout, QWidget, QFrame, QDesktopWidget
from ui.matplotlib_canvas import MatplotlibCanvas


class GridMatrix:
    def __init__(self, workspace_window, size_x=1, size_y=1):
        self.size_x = size_x
        self.size_y = size_y
        self.workspace_window = workspace_window
        self.matrix = [[self._create_canvas_ptl(0, 0)]]
        self.selected_canvas = self.get_canvas(0, 0)
        self.clipboard_visualization_config = None

    def update_matrix_size(self, size_x, size_y):
        if self.size_x < size_x:
            for x in range(self.size_x, size_x):
                self.matrix.append([self._create_canvas_ptl(x, y)
                                   for y in range(self.size_y)])
        elif self.size_x > size_x:
            for x in range(size_x, self.size_x):
                for y in range(self.size_y):
                    self._remove_canvas_ptl(x, y)
            self.matrix = self.matrix[:size_x]

        if self.size_y < size_y:
            for x in range(size_x):
                for y in range(self.size_y, size_y):
                    if x >= len(self.matrix):
                        self.matrix.append([])
                    self.matrix[x].append(self._create_canvas_ptl(x, y))

        elif self.size_y > size_y:
            for x in range(size_x):
                for y in range(size_y, self.size_y):
                    self._remove_canvas_ptl(x, y)
                self.matrix[x] = self.matrix[x][:size_y]

        self.size_x = size_x
        self.size_y = size_y

    def _create_canvas_ptl(self, pos_x, pos_y):
        canvas_container = QWidget()
        layout = QVBoxLayout(canvas_container)
        canvas_container.setLayout(layout)
        canvas = MatplotlibCanvas(
            canvas_container, self.set_selected_canvas, pos_x, pos_y)
        layout.addWidget(canvas)

        screen = QDesktopWidget().screenGeometry()
        min_width = screen.width() // 4
        min_height = screen.height() // 3
        max_width = screen.width()
        max_height = screen.height()
        canvas_container.setMinimumSize(min_width, min_height)
        canvas_container.setMaximumSize(max_width, max_height)

        self.workspace_window.gridt_GS.addWidget(
            canvas_container, pos_x, pos_y)
        return canvas

    def _remove_canvas_ptl(self, pos_x, pos_y):
        canvas_container = self.workspace_window.gridt_GS.itemAtPosition(
            pos_x, pos_y).widget()
        self.workspace_window.gridt_GS.removeWidget(
            canvas_container)
        canvas_container.deleteLater()

    def plot_canvas(self):
        self.clear_selected_canvas()
        self.workspace_window.data_for_chart()
        self.workspace_window.update_tools()

    def remove_all(self):
        for x in range(self.size_x):
            for y in range(self.size_y):
                self._remove_canvas_ptl(x, y)
        self.matrix = [[self._create_canvas_ptl(0, 0)]]
        self.selected_canvas = self.get_canvas(0, 0)
        self.size_x = 1
        self.size_y = 1
        self.workspace_window.size_x_comboboxt_GS.setCurrentIndex(0)
        self.workspace_window.size_y_comboboxt_GS.setCurrentIndex(0)
        self.workspace_window.update_tools()

    def get_canvas(self, pos_x, pos_y):
        return self.matrix[pos_x][pos_y]

    def set_selected_canvas(self, canvas):
        self.selected_canvas = canvas
        self.workspace_window.update_tools()

    def clear_selected_canvas(self):
        pos_x, pos_y = self.selected_canvas.get_position()
        self._remove_canvas_ptl(pos_x, pos_y)
        self.matrix[pos_x][pos_y] = self._create_canvas_ptl(pos_x, pos_y)
        self.selected_canvas = self.matrix[pos_x][pos_y]
        self.workspace_window.update_tools()

    def clear_all_canvases(self):
        for x, row in enumerate(self.matrix):
            for y, canvas in enumerate(row):
                self._remove_canvas_ptl(x, y)
                self.matrix[x][y] = self._create_canvas_ptl(x, y)
        self.workspace_window.update_tools()

    def copy_canvas(self):
        self.clipboard_visualization_config = self.selected_canvas.get_visualization_parameters()
        self.workspace_window.update_tools()

    def paste_canvas(self):

        self.clear_selected_canvas()
        self.selected_canvas.set_visualization_parameters(
            self.clipboard_visualization_config)
        self.selected_canvas.visualization_config.canvas = self.selected_canvas
        self.workspace_window.data_visualizer.plot_copy_chart(
            self.selected_canvas.visualization_config, self.workspace_window.loading)
        self.workspace_window.update_tools()

    def cut_canvas(self):
        self.copy_canvas()
        self.clear_selected_canvas()
        self.workspace_window.update_tools()
