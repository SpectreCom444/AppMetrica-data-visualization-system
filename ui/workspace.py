
from core.shared import shared_state
from visualization.data_visualizer import DataVisualizer
import config.constants as constants
from ui.grid_matrix import GridMatrix
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate
from ui.custom_event_menu import CustomEventMenu
from enums.enums import DisplayMode,HistogramType,Orientation,TypeOfData,GraphType,TypeOfMeasurement,TypeOfCreatingGraph
from config.graph_parameters import graph_parameters

class WorkspaceWindow(QMainWindow):
    def __init__(self):
        super(WorkspaceWindow, self).__init__()
        loadUi('ui/workspace.ui', self)
        self.setWindowTitle("Data visualization system:  Workspace")
        self.data_visualizer =DataVisualizer()
        self.grid_matrix = GridMatrix(self)

        self.create_vizualization_button()
        self.custom_event_menu =CustomEventMenu(self)
        self.showMaximized() 
    
    def set_matrix(self):
        self.grid_matrix.update_matrix_size(int(self.combo_box_height_matrix.currentText()),int(self.combo_box_width_matrix.currentText()))

    def hide_action_button(self):
        self.display_mode.hide()
        self.histogram_type.hide()
        self.orientation.hide()
        self.type_of_measurement.hide()

    def update_action_buttons(self,*args):
        self.hide_action_button()

        for action in graph_parameters[GraphType(self.selected_chart_type.currentText())]:   
            if action == constants.DISPLAY_MODE:
                self.display_mode.show()
            if action == constants.HISTOGRAM_TYPE:
                self.histogram_type.show()
            if action == constants.ORIENTATION:
                self.orientation.show()
            if action == constants.TYPE_OF_MEASUREMENT:
                self.type_of_measurement.show()

    def on_selected_data_change(self, *args):
        self.create_custom_event_menu(self.dropdown_selected_data.currentText() == constants.EVENT_JSON)

    def create_vizualization_button(self):
        self.dropdown_selected_data.addItems(shared_state.ui_names)
        self.dropdown_selected_data.setCurrentText(shared_state.ui_names[0])
        self.dropdown_selected_data.currentTextChanged.connect(self.on_selected_data_change)

        self.selected_chart_type.addItems([graph_type.value for graph_type in GraphType])
        self.selected_chart_type.setCurrentText(next(iter( [graph_type.value for graph_type in GraphType])))
        self.selected_chart_type.currentTextChanged.connect(self.update_action_buttons)
        self.update_action_buttons()

        self.set_grid_size.clicked.connect(self.set_matrix)

        self.plot_button.clicked.connect(lambda: self.data_for_chart(TypeOfCreatingGraph.REPLOAT))
        self.overlay_button.clicked.connect(lambda: self.data_for_chart(TypeOfCreatingGraph.ADD))
        self.delete_all_button.clicked.connect(self.grid_matrix.remove_all)
        self.clear_all_button.clicked.connect(self.grid_matrix.clear_all_canvases)
        self.clear_button.clicked.connect(self.grid_matrix.clear_selected_canvas)
        self.copy_button.clicked.connect(self.grid_matrix.copy_canvas)
        self.insert_button.clicked.connect(self.grid_matrix.paste_canvas)
        self.cut_button.clicked.connect(self.grid_matrix.cut_canvas)
        
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

        self.loader_line.hide()

    
       
        if constants.EVENT_DATATIME in shared_state.names:
            self.set_date_selector(constants.EVENT_DATATIME in shared_state.names)    
        self.create_custom_event_menu(self.dropdown_selected_data.currentText() == constants.EVENT_JSON)

    def loading(self,text):
        if text == constants.END_LOADING:
            self.loader_line.hide()
        else:
            self.loader_line.setText(text)
            if self.loader_line.isHidden():
                self.loader_line.show()
        self.repaint()


    def data_for_chart(self,direction):
        
        self.data_visualizer.set_canvas(self.grid_matrix.selected_canvas)
        self.data_visualizer.set_chart_type([graph_type.value for graph_type in GraphType][self.selected_chart_type.currentIndex()])
        self.data_visualizer.set_other_reference(self.other_reference_slider.value())

        if self.dropdown_selected_data.currentText() == constants.EVENT_JSON:
            if len(self.custom_event_menu.get_selected_options())>0:
                self.data_visualizer.set_type_of_data(TypeOfData.TREE)
                self.data_visualizer.set_selected_data(self.custom_event_menu.get_selected_options() )
            else:
                if constants.EVENT_NAME in shared_state.names :
                   self.data_visualizer.set_type_of_data(TypeOfData.FIELD_NAME)
                   self.data_visualizer.set_selected_data(constants.EVENT_NAME)
        else:
            self.data_visualizer.set_type_of_data(TypeOfData.FIELD_NAME)
            self.data_visualizer.set_selected_data(self.dropdown_selected_data.currentText() )


        if constants.EVENT_DATATIME in shared_state.names:
            self.data_visualizer.set_data_time( self.start_date_entry.date(), self.end_date_entry.date())


        if direction ==TypeOfCreatingGraph.REPLOAT:      
            self.data_visualizer.create_new_plotter()
        elif direction == TypeOfCreatingGraph.ADD:
            pass

        self.data_visualizer.add_chart(self.loading)
    

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