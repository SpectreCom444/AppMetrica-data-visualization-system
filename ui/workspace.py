from PyQt5.QtWidgets import QMainWindow, QApplication, QCheckBox, QPushButton, QVBoxLayout, QWidget, QFrame
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

class WorkspaceWindow(QMainWindow):
    def __init__(self):
        super(WorkspaceWindow, self).__init__()
        loadUi('ui/workspace.ui', self)
        self.checkboxes_layout = QVBoxLayout(self)
