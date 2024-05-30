from ui.interface import create_ui
from shared import shared_state
from PyQt5.QtWidgets import QApplication
from ui.interface import MainWindow
import sys

if __name__ == "__main__":
    # create_ui() 
    #print(shared_state.json_tree)
    if __name__ == '__main__':
        app = QApplication([])
        window = MainWindow()
        window.show()
        sys.exit(app.exec())




        

        