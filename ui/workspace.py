from visualization.data_visualizer import DataVisualizer
import config.constants as constants
from ui.grid_matrix import GridMatrix
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate
from ui.custom_event_menu import CustomEventMenu
from enums import DisplayMode, HistogramType, Orientation, GraphType, TypeOfMeasurement
from config.graph_parameters import graph_parameters


class WorkspaceWindow(QMainWindow):
    def __init__(self, data_storage):
        super(WorkspaceWindow, self).__init__()
        loadUi('ui/workspace.ui', self)
        self.setWindowTitle("Data visualization system:  Workspace")
        self.data_storage = data_storage
        self.data_visualizer = DataVisualizer()
        self.grid_matrix = GridMatrix(self)
        self.create_vizualization_button()
        self.custom_event_menu = CustomEventMenu(self)
        self.showMaximized()

    def set_matrix(self):
        self.grid_matrix.update_matrix_size(int(self.combo_box_height_matrix.currentText(
        )), int(self.combo_box_width_matrix.currentText()))

    def hide_action_button(self):
        self.split_time_mod_panel_VS.hide()
        self.histogram_type_panel_VS.hide()
        self.orientation_type_pane_VS.hide()
        self.type_of_measurement_pane_VS.hide()

    def update_action_buttons(self, *args):
        self.hide_action_button()

        for action in graph_parameters[GraphType(self.chart_type_combo_box_VS.currentText())]:
            if action == constants.DISPLAY_MODE:
                self.split_time_mod_panel_VS.show()
            if action == constants.HISTOGRAM_TYPE:
                self.histogram_type_panel_VS.show()
            if action == constants.ORIENTATION:
                self.orientation_type_pane_VS.show()
            if action == constants.TYPE_OF_MEASUREMENT:
                self.type_of_measurement_pane_VS.show()

    def update_tools(self):
        if self.grid_matrix.clipboard_visualization_config is None:
            self.insert_button_VS.hide()
        else:
            self.insert_button_VS.show()

        if self.grid_matrix.selected_canvas.ax is None:
            self.copy_button_VS.hide()
            self.cut_button_VS.hide()
            self.clear_button_VS.hide()
        else:
            self.copy_button_VS.show()
            self.cut_button_VS.show()
            self.clear_button_VS.show()

    def create_CEM_for_set_metric(self):
        self.visualization_settings_panel.hide()
        self.metrics_list_panel.show()

    def create_vizualization_button(self):

        self.selection_metric_button_VS.clicked.connect(
            self.create_CEM_for_set_metric)

        self.chart_type_combo_box_VS.addItems(
            [graph_type.value for graph_type in GraphType])
        self.chart_type_combo_box_VS.setCurrentText(
            next(iter([graph_type.value for graph_type in GraphType])))
        self.chart_type_combo_box_VS.currentTextChanged.connect(
            self.update_action_buttons)
        self.update_action_buttons()

        self.set_grid_size_buttont_GS.clicked.connect(self.set_matrix)

        self.draw_button_VS.clicked.connect(self.grid_matrix.plot_canvas)
        self.copy_button_VS.clicked.connect(self.grid_matrix.copy_canvas)
        self.insert_button_VS.clicked.connect(self.grid_matrix.paste_canvas)
        self.cut_button_VS.clicked.connect(self.grid_matrix.cut_canvas)
        self.clear_button_VS.clicked.connect(
            self.grid_matrix.clear_selected_canvas)
        self.clear_all_button_VS.clicked.connect(
            self.grid_matrix.clear_all_canvases)
        self.delete_all_button_VS.clicked.connect(self.grid_matrix.remove_all)

        # self.set_type_data_events.clicked.connect(
        #     lambda: self.data_visualizer.set_type_data(constants.EVENTS))
        # self.set_type_data_sessions.clicked.connect(
        #     lambda:  self.data_visualizer.set_type_data(constants.SESSIONS))
        # self.set_type_data_users.clicked.connect(
        #     lambda:  self.data_visualizer.set_type_data(constants.USERS))

        # self.button_split_by_total.clicked.connect(
        #     lambda: self.data_visualizer.set_display_mode(DisplayMode.TOTAL))
        # self.button_split_bu_day.clicked.connect(
        #     lambda:  self.data_visualizer.set_display_mode(DisplayMode.DAY))
        # self.button_split_by_hourse.clicked.connect(
        #     lambda:  self.data_visualizer.set_display_mode(DisplayMode.HOURSE))

        # self.button_summation.clicked.connect(
        #     lambda: self.data_visualizer.set_histogram_type(HistogramType.SUMMATION))
        # self.button_comparison.clicked.connect(
        #     lambda:  self.data_visualizer.set_histogram_type(HistogramType.COMPARISON))

        # self.button_horizontally.clicked.connect(
        #     lambda:  self.data_visualizer.set_orientation(Orientation.HORIZONTAL))
        # self.button_vertically.clicked.connect(
        #     lambda:  self.data_visualizer.set_orientation(Orientation.VERTICAL))

        # self.button_units.clicked.connect(
        #     lambda:  self.data_visualizer.set_type_of_measurement(TypeOfMeasurement.UNITS))
        # self.button_percentages.clicked.connect(
        #     lambda:  self.data_visualizer.set_type_of_measurement(TypeOfMeasurement.PERCENTAGES))

        self.loader_linet_GS.hide()
        self.update_tools()

        self.metrics_list_panel.hide()

        # if constants.EVENT_DATETIME in self.data_storage.names:
        #     self.set_date_selector(
        #         constants.EVENT_DATETIME in self.data_storage.names)

    def loading(self, text):
        if text == constants.END_LOADING:
            self.loader_line.hide()
        else:
            self.loader_line.setText(text)
            if self.loader_line.isHidden():
                self.loader_line.show()
        self.repaint()

    def data_for_chart(self):

        self.data_visualizer.set_canvas(self.grid_matrix.selected_canvas)
        self.data_visualizer.set_chart_type(
            [graph_type.value for graph_type in GraphType][self.selected_chart_type.currentIndex()])
        self.data_visualizer.set_other_reference(
            self.other_reference_slider.value())

        if len(self.custom_event_menu.get_selected_options()) > 0:
            self.data_visualizer.set_selected_data(
                self.custom_event_menu.get_selected_options())

        if constants.EVENT_DATATIME in self.data_storage.names:
            self.data_visualizer.set_data_time(
                self.start_date_entry.date(), self.end_date_entry.date())

        if self.data_visualizer.visualization_config.type_data == constants.EVENTS:
            data = self.data_storage.events_result
        elif self.data_visualizer.visualization_config.type_data == constants.SESSIONS:
            data = self.data_storage.sessions_result
        elif self.data_visualizer.visualization_config.type_data == constants.USERS:
            data = self.data_storage.users_result
        self.data_visualizer.add_chart(self.loading, data)

    def set_date_selector(self, enable: bool):
        self.start_date_combo_box_VS.setDisplayFormat("yyyy-MM-dd")
        self.start_date_combo_box_VS.setDate(QDate.currentDate())

        self.end_date_combo_box_VS.setDisplayFormat("yyyy-MM-dd")
        self.end_date_combo_box_VS.setDate(QDate.currentDate())

        self.start_date_combo_box_VS.setEnabled(enable)
        self.end_date_combo_box_VS.setEnabled(enable)

        self.today_button_VS.clicked.connect(
            lambda: self.set_time_period(QDate.currentDate().addDays(-1)))
        self.last_3_days_button_VS.clicked.connect(
            lambda: self.set_time_period(QDate.currentDate().addDays(-3)))
        self.last_week_button_VS.clicked.connect(
            lambda: self.set_time_period(QDate.currentDate().addDays(-7)))
        self.last_month_button_VS.clicked.connect(
            lambda: self.set_time_period(QDate.currentDate().addMonths(-1)))

    def set_time_period(self, start_date):
        self.start_date_combo_box_VS.setDate(start_date)
        self.end_date_combo_box_VS.setDate(QDate.currentDate())
