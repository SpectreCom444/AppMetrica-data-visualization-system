
from core.data_loader import DataProcessor
from core.shared import shared_state
import config.constants as constants
from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QFileDialog
from PyQt5.uic import loadUi
from ui.workspace import WorkspaceWindow


class DataLoaderWindow(QMainWindow):
    def __init__(self):
        super(DataLoaderWindow, self).__init__()
        loadUi('ui/data-loader.ui', self)
        self.setWindowTitle("Data visualization system")

        self.drop_frame.setAcceptDrops(True)
        self.drop_frame.dragEnterEvent = self.drag_enter_event
        self.drop_frame.dropEvent = self.drop_event
        self.indicator.hide()


        self.drop_frame.mousePressEvent = self.open_file_dialog
        self.showMaximized() 

    def load_data_done(self):
        self.load_data_checkbox.setChecked(True)
        self.repaint()

    def create_events_done(self):
        self.create_events_checkbox.setChecked(True)
        self.repaint()

    def create_session_done(self):
        self.create_sessions_checkbox.setChecked(True)
        self.repaint()

    def create_user_done(self):
        self.create_users_checkbox.setChecked(True)
        self.repaint()


    def uploading_and_processing(self, path):
        self.indicator.show()
        self.repaint()
        processor = DataProcessor(path)
        processor.load_data(self.load_data_done )
        processor.processing_data(self.create_events_done)
        if constants.SESSION_ID in  shared_state.names:
            processor.processing_session(self.create_session_done)

            if constants.DEVICE_ID in  shared_state.names:
                processor.processing_users(self.create_user_done)

        self.window = WorkspaceWindow()
        self.window.show()
        self.close()
       

    def drag_enter_event(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def drop_event(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            self.uploading_and_processing(file_path)

    def open_file_dialog(self, event):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a file", "", "CSV Files (*.csv)", options=options)
        self.uploading_and_processing(file_path)