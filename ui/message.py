from PyQt5.QtWidgets import QMessageBox


def warning_dialog(text):
    msg_box = QMessageBox.warning(
        None, "Warning", text, QMessageBox.Ok | QMessageBox.Cancel)
    if msg_box == QMessageBox.Ok:
        return True
    elif msg_box == QMessageBox.Cancel:
        return False


def warning(text):
    msg_box = QMessageBox.warning(None, "Warning", text)


def error(text):
    QMessageBox.critical(
        None, "Error", f"{str(text)}")
