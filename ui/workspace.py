from typing import List, Callable, Optional
from PyQt5.QtWidgets import QMainWindow, QComboBox, QPushButton, QPlainTextEdit, QSlider, QDateEdit
from PyQt5.QtCore import QDate
from visualization.data_visualizer import DataVisualizer
from PyQt5.uic import loadUi
import config.constants as constants
from ui.grid_matrix import GridMatrix
from ui.message import warning_dialog
from ui.custom_event_menu import CustomEventMenu
from enums import SplitTimeMode, HistogramType, Orientation, GraphType, TypeOfMeasurement, DateType
from config.graph_parameters import graph_parameters
from ui.filter_panel import FilterPanel


class WorkspaceWindow(QMainWindow):
    def __init__(self, data_storage: any) -> None:
        super().__init__()
        loadUi('ui/workspace.ui', self)
        self.setWindowTitle("Data visualization system: Workspace")
        self.data_storage = data_storage
        self._filter_panel = FilterPanel(self.filters_layout_VS, self)
        self.data_visualizer = DataVisualizer(
            self.data_storage, self._filter_panel)
        self._grid_matrix = GridMatrix(self)
        self.custom_event_menu = CustomEventMenu(self)
        self._selected_options: List[str] = []
        self._initialize_ui()

    def _initialize_ui(self) -> None:
        self.showMaximized()
        self._create_vizualization_button()
        self.update_tools()
        self._set_date_selector()
        self.metrics_list_panel.hide()
        self.loader_linet_GS.hide()

    def _create_vizualization_button(self) -> None:
        self._setup_comboboxes()
        self._setup_buttons()
        self._hide_action_button()
        self._update_action_buttons()

    def _setup_comboboxes(self) -> None:
        self._add_items_to_combobox(self.chart_type_combo_box_VS, GraphType)
        self.chart_type_combo_box_VS.currentTextChanged.connect(
            self._update_action_buttons)
        self._update_action_buttons()

        self._add_items_to_combobox(self.data_type_combo_box_VS, DateType)
        self.data_type_combo_box_VS.currentTextChanged.connect(
            self._set_date_type)

        self._add_items_to_combobox(
            self.split_time_mod_combo_box_VS, SplitTimeMode)
        self.split_time_mod_combo_box_VS.currentTextChanged.connect(
            self._set_split_time_mode)

        self._add_items_to_combobox(
            self.histogram_type_combo_box_VS, HistogramType)
        self.histogram_type_combo_box_VS.currentTextChanged.connect(
            self._set_histogram_type)

        self._add_items_to_combobox(
            self.orientation_type_combo_box_VS, Orientation)
        self.orientation_type_combo_box_VS.currentTextChanged.connect(
            self._set_orientation)

        self._add_items_to_combobox(
            self.type_of_measurement_combo_box_VS, TypeOfMeasurement)
        self.type_of_measurement_combo_box_VS.currentTextChanged.connect(
            self._set_type_of_measurement)

    def _setup_buttons(self) -> None:
        self.set_grid_size_buttont_GS.clicked.connect(self._set_matrix)
        self.back_to_uploading_data_button_VS.clicked.connect(
            self._back_button_clicked)
        self.draw_button_VS.clicked.connect(self._grid_matrix.plot_canvas)
        self.copy_button_VS.clicked.connect(self._grid_matrix.copy_canvas)
        self.insert_button_VS.clicked.connect(self._grid_matrix.paste_canvas)
        self.cut_button_VS.clicked.connect(self._grid_matrix.cut_canvas)
        self.clear_button_VS.clicked.connect(
            self._grid_matrix.clear_selected_canvas)
        self.clear_all_button_VS.clicked.connect(
            self._grid_matrix.clear_all_canvases)
        self.delete_all_button_VS.clicked.connect(self._grid_matrix.remove_all)
        self.add_filter_button_VS.clicked.connect(
            self._filter_panel.add_filter)
        self.treshold_slider_VS.valueChanged.connect(
            self._slider_value_changed)
        self.selection_metric_button_VS.clicked.connect(
            self.create_CEM_for_set_metric)

    def _add_items_to_combobox(self, combobox: QComboBox, enum_class: any) -> None:
        combobox.addItems([item.value for item in enum_class])
        combobox.setCurrentText(
            next(iter([item.value for item in enum_class])))

    def _set_matrix(self) -> None:
        self._grid_matrix.update_matrix_size(
            int(self.size_x_comboboxt_GS.currentText()),
            int(self.size_y_comboboxt_GS.currentText())
        )

    def _hide_action_button(self) -> None:
        self.split_time_mod_panel_VS.hide()
        self.histogram_type_panel_VS.hide()
        self.orientation_type_pane_VS.hide()
        self.type_of_measurement_pane_VS.hide()

    def _update_action_buttons(self) -> None:
        self._hide_action_button()
        actions = graph_parameters[GraphType(
            self.chart_type_combo_box_VS.currentText())]
        self._update_visibility(
            self.split_time_mod_panel_VS, constants.SPLIT_TIME_MODE, actions)
        self._update_visibility(
            self.histogram_type_panel_VS, constants.HISTOGRAM_TYPE, actions)
        self._update_visibility(
            self.orientation_type_pane_VS, constants.ORIENTATION, actions)
        self._update_visibility(
            self.type_of_measurement_pane_VS, constants.TYPE_OF_MEASUREMENT, actions)

    def _update_visibility(self, panel: any, action: str, actions: List[str]) -> None:
        if action in actions:
            panel.show()
        else:
            panel.hide()

    def update_tools(self) -> None:
        self._toggle_button_visibility(
            self.insert_button_VS, self._grid_matrix.clipboard_visualization_config is not None)
        self._toggle_button_visibility(
            self.copy_button_VS, self._grid_matrix.selected_canvas.ax is not None)
        self._toggle_button_visibility(
            self.cut_button_VS, self._grid_matrix.selected_canvas.ax is not None)
        self._toggle_button_visibility(
            self.clear_button_VS, self._grid_matrix.selected_canvas.ax is not None)

    def _toggle_button_visibility(self, button: QPushButton, condition: bool) -> None:
        button.setVisible(condition)

    def _back_button_clicked(self) -> None:
        if warning_dialog('Are you sure you want to go back? Any unsaved changes will be lost.'):
            from ui.data_loader_interface import DataLoaderWindow
            self.data_loader_window = DataLoaderWindow(self.data_storage)
            self.data_loader_window.show()
            self.hide()

    def create_CEM_for_set_metric(self) -> None:
        self.visualization_settings_panel.hide()
        self.metrics_list_panel.show()
        self.custom_event_menu.set_parameters(
            self._apply_selected_options, self._selected_options)

    def _set_date_type(self) -> None:
        self.data_visualizer.set_type_data(
            DateType(self.data_type_combo_box_VS.currentText()))

    def _set_split_time_mode(self) -> None:
        self.data_visualizer.set_split_time_mode(SplitTimeMode(
            self.split_time_mod_combo_box_VS.currentText()))

    def _set_histogram_type(self) -> None:
        self.data_visualizer.set_histogram_type(HistogramType(
            self.histogram_type_combo_box_VS.currentText()))

    def _set_orientation(self) -> None:
        self.data_visualizer.set_orientation(Orientation(
            self.orientation_type_combo_box_VS.currentText()))

    def _set_type_of_measurement(self) -> None:
        self.data_visualizer.set_type_of_measurement(TypeOfMeasurement(
            self.type_of_measurement_combo_box_VS.currentText()))

    def _apply_selected_options(self, selected_options: List[str]) -> None:
        self._selected_options = selected_options
        self.path_text_VS.clear()
        for i, option in enumerate(self._selected_options):
            indent = '    ' * i
            self.path_text_VS.appendPlainText(
                f"{indent}﹂{str(option)}" if i > 0 else f"{indent}{str(option)}")

    def _slider_value_changed(self) -> None:
        value = self.treshold_slider_VS.value()
        self.treshold_value_VS.setText(f"{round(value / 10, 1)}%")

    def loading(self, text: str) -> None:
        if text == constants.END_LOADING:
            self.loader_linet_GS.hide()
        else:
            self.loader_linet_GS.setText(text)
            self.loader_linet_GS.setVisible(True)
        self.repaint()

    def data_for_chart(self) -> None:
        self.data_visualizer.set_canvas(self._grid_matrix.selected_canvas)
        self.data_visualizer.set_chart_type(
            [chart_type.value for chart_type in GraphType][self.chart_type_combo_box_VS.currentIndex()]
        )
        self.data_visualizer.set_treshold_reference(
            self.treshold_slider_VS.value())
        self.data_visualizer.set_selected_options(self._selected_options)
        self.data_visualizer.set_data_time(
            self.start_date_combo_box_VS.date(), self.end_date_combo_box_VS.date())
        self.data_visualizer.add_chart(self.loading)

    def _set_date_selector(self) -> None:
        self._setup_date_combobox(self.start_date_combo_box_VS)
        self._setup_date_combobox(self.end_date_combo_box_VS)
        self.today_button_VS.clicked.connect(
            lambda: self._set_time_period(QDate.currentDate().addDays(-1)))
        self.last_3_days_button_VS.clicked.connect(
            lambda: self._set_time_period(QDate.currentDate().addDays(-3)))
        self.last_week_button_VS.clicked.connect(
            lambda: self._set_time_period(QDate.currentDate().addDays(-7)))
        self.last_month_button_VS.clicked.connect(
            lambda: self._set_time_period(QDate.currentDate().addMonths(-1)))

    def _setup_date_combobox(self, combobox: QDateEdit) -> None:
        combobox.setDisplayFormat("yyyy-MM-dd")
        combobox.setDate(QDate.currentDate())

    def _set_time_period(self, start_date: QDate) -> None:
        self.start_date_combo_box_VS.setDate(start_date)
        self.end_date_combo_box_VS.setDate(QDate.currentDate())
