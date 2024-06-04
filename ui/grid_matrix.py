from PyQt5.QtWidgets import QMainWindow, QApplication, QCheckBox, QPushButton, QVBoxLayout, QWidget, QFrame
from ui.matplotlib_canvas import MatplotlibCanvas

class GridMatrix:
    def __init__(self, workspace_window, size_x=1, size_y=1):
        self.size_x = size_x
        self.size_y = size_y
        self.workspace_window = workspace_window
        self.matrix = [[self.create_canvas_ptl(0, 0)]]
        self.selected_canvas = self.get_canvas(0, 0)
        self.clipboard_visualization_config = None 

    def update_matrix_size(self, size_x, size_y):
        if self.size_x < size_x:
            for x in range(self.size_x, size_x):
                self.matrix.append([self.create_canvas_ptl(x, y) for y in range(self.size_y)])
        elif self.size_x > size_x:
            for x in range(size_x, self.size_x):
                for y in range(self.size_y):
                    self.remove_canvas_ptl(x, y)
            self.matrix = self.matrix[:size_x]

        if self.size_y < size_y:
            for x in range(size_x):
                for y in range(self.size_y, size_y):
                    if x >= len(self.matrix):
                        self.matrix.append([])
                    self.matrix[x].append(self.create_canvas_ptl(x, y))
        elif self.size_y > size_y:
            for x in range(size_x):
                for y in range(size_y, self.size_y):
                    self.remove_canvas_ptl(x, y)
                self.matrix[x] = self.matrix[x][:size_y]

        self.size_x = size_x
        self.size_y = size_y

    def create_canvas_ptl(self, pos_x, pos_y):
        canvas_container = QWidget()
        layout = QVBoxLayout(canvas_container)
        canvas_container.setLayout(layout)
        canvas = MatplotlibCanvas(canvas_container, self.set_selected_canvas, pos_x, pos_y)
        layout.addWidget(canvas)
        canvas_container.setMinimumSize(360,360)
        canvas_container.setMaximumSize(1080,1080)

        self.workspace_window.canvas_container_layout.addWidget(canvas_container, pos_x, pos_y)
        return canvas

    def remove_canvas_ptl(self, pos_x, pos_y):
        canvas_container = self.workspace_window.canvas_container_layout.itemAtPosition(pos_x, pos_y).widget()
        self.workspace_window.canvas_container_layout.removeWidget(canvas_container)
        canvas_container.deleteLater()

    def remove_all(self):
        for x in range(self.size_x):
            for y in range(self.size_y):
                self.remove_canvas_ptl(x, y)
        self.matrix = [[self.create_canvas_ptl(0, 0)]]
        self.selected_canvas = self.get_canvas(0, 0)
        self.size_x = 1
        self.size_y = 1
        self.workspace_window.combo_box_height_matrix.setCurrentIndex(0)
        self.workspace_window.combo_box_width_matrix.setCurrentIndex(0)

    def get_canvas(self, pos_x, pos_y):
        return self.matrix[pos_x][pos_y]

    def set_selected_canvas(self, canvas):
        self.selected_canvas = canvas

    def clear_selected_canvas(self):
        pos_x, pos_y = self.selected_canvas.get_position()
        self.remove_canvas_ptl(pos_x, pos_y)
        self.matrix[pos_x][pos_y] = self.create_canvas_ptl(pos_x, pos_y)
        self.selected_canvas = self.matrix[pos_x][pos_y]

    def clear_all_canvases(self):
        for x, row in enumerate(self.matrix):
            for y, canvas in enumerate(row):
                self.remove_canvas_ptl(x, y)
                self.matrix[x][y] = self.create_canvas_ptl(x, y)

    def copy_canvas(self):
        self.clipboard_visualization_config= self.selected_canvas.get_visualization_parameters()
        print("copy")

    def paste_canvas(self):
       
        self.clear_selected_canvas()
        self.selected_canvas.set_visualization_parameters(self.clipboard_visualization_config)
        self.selected_canvas.visualization_config.canvas = self.selected_canvas
        self.workspace_window.data_visualizer.plot_copy_chart(self.selected_canvas.visualization_config)

        print("past")

    def cut_canvas(self):
        self.copy_canvas()
        self.clear_selected_canvas()