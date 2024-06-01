from matplotlib.figure import Figure
from shared import shared_state
from visualization import create_chart
from tkcalendar import DateEntry
import type_graphs
import constants
from visualization_params import VisualizationParams
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QMainWindow, QApplication, QCheckBox, QPushButton, QVBoxLayout, QWidget, QFrame
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate
from PyQt5 import QtWidgets
from enums import DisplayMode,HistogramType,Orientation,TypeOfData


class MatplotlibCanvas(FigureCanvasQTAgg):
    def __init__(self, parent):
        fig = Figure()
        self.fig = Figure()
        super(MatplotlibCanvas, self).__init__(self.fig)
        self.setParent(parent)

class WorkspaceWindow(QMainWindow):
    def __init__(self):
        super(WorkspaceWindow, self).__init__()
        loadUi('ui/workspace.ui', self)
        self.visualization_params=VisualizationParams()
        self.create_vizualization_button()
        self.custom_event_menu =CustomEventMenu(self)
        self.showMaximized() 

    def create_canvas_ptl_down(self):
        row_count = self.canvas_container_layout.rowCount()
        canvas_container = QWidget()
        layout = QVBoxLayout(canvas_container)
        canvas_container.setLayout(layout)
        canvas = MatplotlibCanvas(canvas_container)
        layout.addWidget(canvas)
        self.canvas_container_layout.addWidget(canvas_container, row_count, 0)

        return canvas

    def create_canvas_ptl_right(self):
        column_count = self.canvas_container_layout.columnCount()
        canvas_container = QWidget()
        layout = QVBoxLayout(canvas_container)
        canvas_container.setLayout(layout)
        canvas = MatplotlibCanvas(canvas_container)
        layout.addWidget(canvas)
        self.canvas_container_layout.addWidget(canvas_container, 0, column_count)

        return canvas

    def create_vizualization_button(self):
        def on_selected_data_change(*args):
            self.create_custom_event_menu(self.dropdown_selected_data.currentText() == constants.EVENT_JSON)

        self.dropdown_selected_data.addItems(shared_state.names)
        self.dropdown_selected_data.setCurrentText(shared_state.names[0])
        self.dropdown_selected_data.currentTextChanged.connect(on_selected_data_change)

        self.selected_chart_type.addItems(type_graphs.TYPES_GRAPHS.keys())
        self.selected_chart_type.setCurrentText(next(iter(type_graphs.TYPES_GRAPHS)))
        self.selected_chart_type.currentTextChanged.connect(on_selected_data_change)

        self.plot_button.clicked.connect(lambda: self.data_for_chart("down"))
        self.plot_button_right.clicked.connect(lambda: self.data_for_chart("right"))
        self.clear_button.clicked.connect(self.clear_all)
        

        self.button_split_by_total.clicked.connect(lambda: self.visualization_params.set_display_mode(DisplayMode.TOTAL))
        self.button_split_bu_day.clicked.connect(lambda:  self.visualization_params.set_display_mode(DisplayMode.DAY))
        self.button_split_by_hourse.clicked.connect(lambda:  self.visualization_params.set_display_mode(DisplayMode.HOURSE))

        self.button_summation.clicked.connect(lambda: self.visualization_params.set_histogram_type(HistogramType.SUMMATION))
        self.button_comparison.clicked.connect(lambda:  self.visualization_params.set_histogram_type(HistogramType.COMPARISON))

        self.button_horizontally.clicked.connect(lambda:  self.visualization_params.set_orientation(Orientation.HORIZONTAL))
        self.button_vertically.clicked.connect(lambda:  self.visualization_params.set_orientation(Orientation.VERTICAL))

        if constants.EVENT_DATATIME in shared_state.names:
            self.set_date_selector(constants.EVENT_DATATIME in shared_state.names)    
        self.create_custom_event_menu(self.dropdown_selected_data.currentText() == constants.EVENT_JSON)

    def clear_all(self):
        for i in reversed(range(self.canvas_container_layout.count())):
            widget = self.canvas_container_layout.itemAt(i).widget()
            self.canvas_container_layout.removeWidget(widget)
            widget.deleteLater()

    def data_for_chart(self,direction):
        if direction == "down":
            canvas = self.create_canvas_ptl_down()
        elif direction == "right":
            canvas = self.create_canvas_ptl_right()

        if self.dropdown_selected_data.currentText() == constants.EVENT_JSON:
            if len(self.custom_event_menu.get_selected_options())>0:
                self.visualization_params.set_data_to_display(TypeOfData.TREE,canvas,self.custom_event_menu.get_selected_options(),type_graphs.TYPES_GRAPHS[self.selected_chart_type.currentText()],self.other_reference_slider.value() )
            else:
                if constants.EVENT_NAME in shared_state.names :
                    self.visualization_params.set_data_to_display(TypeOfData.FIELD_NAME,canvas,constants.EVENT_NAME,type_graphs.TYPES_GRAPHS[self.selected_chart_type.currentText()],self.other_reference_slider.value() )
        else:
            self.visualization_params.set_data_to_display(TypeOfData.FIELD_NAME,canvas,self.dropdown_selected_data.currentText(),type_graphs.TYPES_GRAPHS[self.selected_chart_type.currentText()],self.other_reference_slider.value() )


        if constants.EVENT_DATATIME in shared_state.names:
            self.visualization_params.set_data_time( self.start_date_entry.date(), self.end_date_entry.date())

        create_chart(self.visualization_params)

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
