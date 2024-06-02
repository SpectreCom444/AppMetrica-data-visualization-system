from matplotlib.figure import Figure
from core.shared import shared_state
from visualization.data_visualizer import DataVisualizer
import config.constants as constants
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QMainWindow, QApplication, QCheckBox, QPushButton, QVBoxLayout, QWidget, QFrame
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate
from PyQt5 import QtWidgets
from enums.enums import DisplayMode,HistogramType,Orientation,TypeOfData,GraphType,TypeOfMeasurement


class MatplotlibCanvas(FigureCanvasQTAgg):
    def __init__(self, parent, on_click_callback,pos_x,pos_y):
        self.fig = Figure()
        super(MatplotlibCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.on_click_callback = on_click_callback
        self.mpl_connect("button_press_event", self.on_click)
        self.is_graph_displayed = False
        self.pos_x=pos_x
        self.pos_y = pos_y

    def get_position(self):
        return (self.pos_x,self.pos_y)
    
    def on_click(self, event):
        self.on_click_callback(self)

class GridMatrix:
    def __init__(self,workspace_window, size_x = 1,size_y = 1):
        self.size_x = size_x
        self.size_y = size_y
        self.workspace_window=workspace_window
        self.matrix = [[self.create_canvas_ptl(0,0)]]
        self.selected_canvas=self.get_canvas(0,0)
    
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
        canvas = MatplotlibCanvas(canvas_container, self.set_selected_canvas,pos_x, pos_y)
        layout.addWidget(canvas)
        canvas.setFixedSize(800, 600)
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
        self.selected_canvas =self.get_canvas(0,0)
        self.size_x = 1
        self.size_y = 1
        self.workspace_window.combo_box_height_matrix.setCurrentIndex(0)
        self.workspace_window.combo_box_width_matrix.setCurrentIndex(0)
    
    def get_canvas(self, pos_x, pos_y):
        return self.matrix[pos_x][pos_y]
    
    def set_selected_canvas(self, canvas):
        self.selected_canvas = canvas

    def clear_selected_canvas(self):
        pos_x,pos_y =self.selected_canvas.get_position()
        self.remove_canvas_ptl(pos_x, pos_y)
        self.matrix[pos_x][pos_y] = self.create_canvas_ptl(pos_x, pos_y)
        self.selected_canvas = self.matrix[pos_x][pos_y]

    def clear_all_canvases(self):
        for x, row in enumerate(self.matrix):
            for y, canvas in enumerate(row):
                self.remove_canvas_ptl(x, y)
                self.matrix[x][y] = self.create_canvas_ptl(x, y)

class WorkspaceWindow(QMainWindow):
    def __init__(self):
        super(WorkspaceWindow, self).__init__()
        loadUi('ui/workspace.ui', self)
        self.data_visualizer =DataVisualizer()
        self.grid_matrix = GridMatrix(self)

        self.create_vizualization_button()
        self.custom_event_menu =CustomEventMenu(self)
        self.showMaximized() 
    
    def set_matrix(self):
        self.grid_matrix.update_matrix_size(int(self.combo_box_height_matrix.currentText()),int(self.combo_box_width_matrix.currentText()))

    def create_vizualization_button(self):
        def on_selected_data_change(*args):
            self.create_custom_event_menu(self.dropdown_selected_data.currentText() == constants.EVENT_JSON)

        self.dropdown_selected_data.addItems(shared_state.ui_names)
        self.dropdown_selected_data.setCurrentText(shared_state.ui_names[0])
        self.dropdown_selected_data.currentTextChanged.connect(on_selected_data_change)

        self.selected_chart_type.addItems([graph_type.value for graph_type in GraphType])
        self.selected_chart_type.setCurrentText(next(iter( [graph_type.value for graph_type in GraphType])))

        self.set_grid_size.clicked.connect(self.set_matrix)

        self.plot_button.clicked.connect(lambda: self.data_for_chart("replot"))
        self.overlay_button.clicked.connect(lambda: self.data_for_chart("add"))
        self.delete_all_button.clicked.connect(self.grid_matrix.remove_all)
        
        self.set_type_data_events.clicked.connect(lambda: self.data_visualizer.set_type_data(constants.EVENTS))
        self.set_type_data_sessions.clicked.connect(lambda:  self.data_visualizer.set_type_data(constants.SESSIONS))
        self.set_type_data_users.clicked.connect(lambda:  self.data_visualizer.set_type_data(constants.USERS))

        self.button_split_by_total.clicked.connect(lambda: self.data_visualizer.set_display_mode(DisplayMode.TOTAL))
        self.button_split_bu_day.clicked.connect(lambda:  self.data_visualizer.set_display_mode(DisplayMode.DAY))
        self.button_split_by_hourse.clicked.connect(lambda:  self.data_visualizer.set_display_mode(DisplayMode.HOURSE))

        self.button_summation.clicked.connect(lambda: self.data_visualizer.set_histogram_type(HistogramType.SUMMATION))
        self.button_comparison.clicked.connect(lambda:  self.data_visualizer.set_histogram_type(HistogramType.COMPARISON))

        self.button_horizontally.clicked.connect(lambda:  self.data_visualizer.set_orientation(Orientation.HORIZONTAL))
        self.button_vertically.clicked.connect(lambda:  self.data_visualizer.set_orientation(Orientation.VERTICAL))

        self.button_units.clicked.connect(lambda:  self.data_visualizer.set_type_of_measurement(TypeOfMeasurement.UNITS))
        self.button_percentages.clicked.connect(lambda:  self.data_visualizer.set_type_of_measurement(TypeOfMeasurement.PERCENTAGES))

        self.clear_all_button.clicked.connect(self.grid_matrix.clear_all_canvases)
        self.clear_button.clicked.connect(self.grid_matrix.clear_selected_canvas)

       
        if constants.EVENT_DATATIME in shared_state.names:
            self.set_date_selector(constants.EVENT_DATATIME in shared_state.names)    
        self.create_custom_event_menu(self.dropdown_selected_data.currentText() == constants.EVENT_JSON)

    

    def data_for_chart(self,direction):
        if self.dropdown_selected_data.currentText() == constants.EVENT_JSON:
            if len(self.custom_event_menu.get_selected_options())>0:
                self.data_visualizer.set_data_to_display(TypeOfData.TREE,self.grid_matrix.selected_canvas,self.custom_event_menu.get_selected_options(),[graph_type.value for graph_type in GraphType][self.selected_chart_type.currentIndex()],self.other_reference_slider.value() )
            else:
                if constants.EVENT_NAME in shared_state.names :
                    self.data_visualizer.set_data_to_display(TypeOfData.FIELD_NAME,self.grid_matrix.selected_canvas,constants.EVENT_NAME,[graph_type.value for graph_type in GraphType][self.selected_chart_type.currentIndex()],self.other_reference_slider.value() )
        else:
            self.data_visualizer.set_data_to_display(TypeOfData.FIELD_NAME,self.grid_matrix.selected_canvas,self.dropdown_selected_data.currentText(),[graph_type.value for graph_type in GraphType][self.selected_chart_type.currentIndex()],self.other_reference_slider.value() )


        if constants.EVENT_DATATIME in shared_state.names:
            self.data_visualizer.set_data_time( self.start_date_entry.date(), self.end_date_entry.date())


        if direction =="replot":      
            self.data_visualizer.create_new_plotter(self.data_visualizer)
        elif direction == "add":
            pass

        self.data_visualizer.add_chart(self.data_visualizer)
        self.grid_matrix.selected_canvas.draw()

    def set_date_selector(self, enable: bool):
        self.start_date_entry.setDisplayFormat("yyyy-MM-dd")
        self.start_date_entry.setDate(QDate.currentDate())

        self.end_date_entry.setDisplayFormat("yyyy-MM-dd")
        self.end_date_entry.setDate(QDate.currentDate())

        self.start_date_entry.setEnabled(enable)
        self.end_date_entry.setEnabled(enable)

        self.today_button.clicked.connect(lambda: self.set_time_period(QDate.currentDate().addDays(-1)))
        self.last_3_days_button.clicked.connect(lambda: self.set_time_period(QDate.currentDate().addDays(-3)))
        self.last_week_button.clicked.connect(lambda: self.set_time_period(QDate.currentDate().addDays(-7)))
        self.last_month_button.clicked.connect(lambda: self.set_time_period(QDate.currentDate().addMonths(-1)))


    def create_custom_event_menu(self, show):
        if show:
            self.group_box_json_buttons.show()
        else:
            self.group_box_json_buttons.hide()

    def set_time_period(self,start_date):
        self.start_date_entry.setDate(start_date)
        self.end_date_entry.setDate(QDate.currentDate())

            

   

class CustomEventMenu:
    def __init__(self,workspace_window):

        self.matrix_of_buttons_grid= workspace_window.matrix_of_buttons_grid
        self.dictionary_path=workspace_window.dictionary_path
        self.undo_button= workspace_window.undo_button
        self.undo_button.clicked.connect(self.undo_last_selection)        
        self.selected_options = []
        self.current_options = list(shared_state.json_tree.keys())
        self.update_buttons()  
    
    def update_buttons(self):        

        for i in reversed(range(self.matrix_of_buttons_grid.count())):
            widget = self.matrix_of_buttons_grid.itemAt(i).widget()
            if isinstance(widget, QtWidgets.QPushButton) and widget != self.undo_button:
                widget.deleteLater()
        
        current_level = shared_state.json_tree
        for opt in self.selected_options:
            if isinstance(current_level, dict):
                current_level = current_level.get(opt, {})
            else:
                current_level = {}
                break
        
        for idx, option in enumerate(self.current_options):     
            has_children = isinstance(current_level.get(option, {}), dict) and bool(current_level.get(option, {}))
            button = QtWidgets.QPushButton(option)
            button.setEnabled(has_children)
            button.clicked.connect(self.create_button_handler(option))
            self.matrix_of_buttons_grid.addWidget(button)

    def create_button_handler(self, option):
        def handler():
            self.add_to_selected(option)
        return handler
    
    def add_to_selected(self, option):
        if option not in self.selected_options:
            self.selected_options.append(option)
            self.update_text_widget()
            self.update_options()

    def undo_last_selection(self):
        if self.selected_options:
            self.selected_options.pop()
            self.update_text_widget()
            self.update_options()

    def update_options(self):
        current_level = shared_state.json_tree
        for opt in self.selected_options:
            if isinstance(current_level, dict):
                current_level = current_level.get(opt, {})
            else:
                current_level = {}
                break

        if isinstance(current_level, dict):
            self.current_options = list(current_level.keys())
        else:
            self.current_options = [current_level]
        self.update_buttons()
    
    def update_text_widget(self):
        self.dictionary_path.clear()
        for option in self.selected_options:
            self.dictionary_path.setText(self.dictionary_path.text() + str(option) + '->')

    def get_selected_options(self):
        return self.selected_options 
