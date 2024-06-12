from visualization.data_visualizer import DataVisualizer
import config.constants as constants
from ui.grid_matrix import GridMatrix
from ui.message import warning_dialog
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate
from ui.custom_event_menu import CustomEventMenu
from enums import SplitTimeMode, HistogramType, Orientation, GraphType, TypeOfMeasurement, DateType
from config.graph_parameters import graph_parameters
from ui.filter_panel import FilterPanel


class WorkspaceWindow(QMainWindow):
    def __init__(self, data_storage):
        super(WorkspaceWindow, self).__init__()
        loadUi('ui/workspace.ui', self)
        self.setWindowTitle("Data visualization system:  Workspace")
        self.data_storage = data_storage
        self.filter_panel = FilterPanel(self.filters_layout_VS, self)
        self.data_visualizer = DataVisualizer(
            self.data_storage, self.filter_panel)
        self.grid_matrix = GridMatrix(self)
        self.create_vizualization_button()
        self.custom_event_menu = CustomEventMenu(self)
        self.showMaximized()
        self.selected_options = []

    def set_matrix(self):
        self.grid_matrix.update_matrix_size(int(self.size_x_comboboxt_GS.currentText(
        )), int(self.size_y_comboboxt_GS.currentText()))

    def hide_action_button(self):
        self.split_time_mod_panel_VS.hide()
        self.histogram_type_panel_VS.hide()
        self.orientation_type_pane_VS.hide()
        self.type_of_measurement_pane_VS.hide()

    def update_action_buttons(self, *args):
        self.hide_action_button()

        for action in graph_parameters[GraphType(self.chart_type_combo_box_VS.currentText())]:
            if action == constants.SPLIT_TIME_MODE:
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

    def back_button_clicked(self):
        if warning_dialog(f'Are you sure you want to go back? Any unsaved changes will be lost.'):
            from ui.data_loader_interface import DataLoaderWindow
            self.data_loader_window = DataLoaderWindow(self.data_storage)
            self.data_loader_window.show()
            self.hide()

    def create_CEM_for_set_metric(self):
        self.visualization_settings_panel.hide()
        self.metrics_list_panel.show()
        self.custom_event_menu.set_parameters(
            self.applay_selected_options, self.selected_options)

    def set_date_type(self):
        self.data_visualizer.set_type_data(
            DateType(self.data_type_combo_box_VS.currentText()))

    def set_display_mode(self):
        self.data_visualizer.set_display_mode(
            SplitTimeMode(self.split_time_mod_combo_box_VS.currentText()))

    def set_histogram_type(self):
        self.data_visualizer.set_histogram_type(
            HistogramType(self.histogram_type_combo_box_VS.currentText()))

    def set_orientation(self):
        self.data_visualizer.set_orientation(
            Orientation(self.orientation_type_combo_box_VS.currentText()))

    def set_type_of_measurement(self):
        self.data_visualizer.set_type_of_measurement(
            TypeOfMeasurement(self.type_of_measurement_combo_box_VS.currentText()))

    def applay_selected_options(self, selected_options):
        self.selected_options = selected_options
        self.path_text_VS.clear()
        for i, option in enumerate(self.selected_options):
            indent = '    ' * i
            self.path_text_VS.appendPlainText(
                f"{indent}﹂{str(option)}" if i > 0 else f"{indent}{str(option)}")

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

        self.back_to_uploading_data_button_VS.clicked.connect(
            self.back_button_clicked)
        self.draw_button_VS.clicked.connect(self.grid_matrix.plot_canvas)
        self.copy_button_VS.clicked.connect(self.grid_matrix.copy_canvas)
        self.insert_button_VS.clicked.connect(self.grid_matrix.paste_canvas)
        self.cut_button_VS.clicked.connect(self.grid_matrix.cut_canvas)
        self.clear_button_VS.clicked.connect(
            self.grid_matrix.clear_selected_canvas)
        self.clear_all_button_VS.clicked.connect(
            self.grid_matrix.clear_all_canvases)
        self.delete_all_button_VS.clicked.connect(self.grid_matrix.remove_all)
        self.add_filter_button_VS.clicked.connect(self.filter_panel.add_filter)

        self.data_type_combo_box_VS.addItems(
            [date_type.value for date_type in DateType])
        self.data_type_combo_box_VS.setCurrentText(
            next(iter([date_type.value for date_type in DateType])))
        self.data_type_combo_box_VS.currentTextChanged.connect(
            self.set_date_type)

        self.split_time_mod_combo_box_VS.addItems(
            [mode.value for mode in SplitTimeMode])
        self.split_time_mod_combo_box_VS.setCurrentText(
            next(iter([mode.value for mode in SplitTimeMode])))
        self.split_time_mod_combo_box_VS.currentTextChanged.connect(
            self.set_display_mode)

        self.histogram_type_combo_box_VS.addItems(
            [histogram_type.value for histogram_type in HistogramType])
        self.histogram_type_combo_box_VS.setCurrentText(
            next(iter([histogram_type.value for histogram_type in HistogramType])))
        self.histogram_type_combo_box_VS.currentTextChanged.connect(
            self.set_histogram_type)

        self.orientation_type_combo_box_VS.addItems(
            [orientation.value for orientation in Orientation])
        self.orientation_type_combo_box_VS.setCurrentText(
            next(iter([orientation.value for orientation in Orientation])))
        self.orientation_type_combo_box_VS.currentTextChanged.connect(
            self.set_orientation)

        self.type_of_measurement_combo_box_VS.addItems(
            [type_of_measurement.value for type_of_measurement in TypeOfMeasurement])
        self.type_of_measurement_combo_box_VS.setCurrentText(
            next(iter([type_of_measurement.value for type_of_measurement in TypeOfMeasurement])))
        self.type_of_measurement_combo_box_VS.currentTextChanged.connect(
            self.set_type_of_measurement)

        self.treshold_slider_VS.valueChanged.connect(self.sliderValueChanged)
        self.loader_linet_GS.hide()
        self.update_tools()

        self.metrics_list_panel.hide()

        self.set_date_selector()

    def sliderValueChanged(self):
        value = self.treshold_slider_VS.value()
        self.treshold_value_VS.setText(f"{round(value/10, 1)}%")

    def loading(self, text):
        if text == constants.END_LOADING:
            self.loader_linet_GS.hide()
        else:
            self.loader_linet_GS.setText(text)
            if self.loader_linet_GS.isHidden():
                self.loader_linet_GS.show()
        self.repaint()

    def data_for_chart(self):

        self.data_visualizer.set_canvas(self.grid_matrix.selected_canvas)
        self.data_visualizer.set_chart_type(
            [graph_type.value for graph_type in GraphType][self.chart_type_combo_box_VS.currentIndex()])
        self.data_visualizer.set_other_reference(
            self.treshold_slider_VS.value())
        self.data_visualizer.set_selected_data(self.selected_options)

        self.data_visualizer.set_data_time(
            self.start_date_combo_box_VS.date(), self.end_date_combo_box_VS.date())

        self.data_visualizer.add_chart(self.loading)

    def set_date_selector(self):
        self.start_date_combo_box_VS.setDisplayFormat("yyyy-MM-dd")
        self.start_date_combo_box_VS.setDate(QDate.currentDate())

        self.end_date_combo_box_VS.setDisplayFormat("yyyy-MM-dd")
        self.end_date_combo_box_VS.setDate(QDate.currentDate())

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
