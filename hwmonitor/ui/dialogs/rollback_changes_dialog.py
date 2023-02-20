from PySide2.QtCore import Qt, QTimer
from PySide2.QtGui import QShowEvent
from PySide2.QtWidgets import QMessageBox


class RollbackChangesDialog(QMessageBox):

    def __init__(self, timeout=20, parent=None):
        super().__init__(parent)
        self.timeout = timeout

        self.setWindowTitle("Keep Change?")
        self.setWindowFlags(Qt.Dialog
                            | Qt.CustomizeWindowHint
                            | Qt.WindowTitleHint
                            | Qt.MSWindowsFixedSizeDialogHint
                            | Qt.WindowStaysOnTopHint)

        self.setIcon(QMessageBox.Warning)
        self.setText("Your desktop configuration has changed.\n"
                     "Would you like to keep this change?")
        self.setInformativeText(f"Reverting in {self.timeout} Seconds")
        self.setStandardButtons(QMessageBox.Yes |
                                QMessageBox.No)
        self.setDefaultButton(QMessageBox.No)

        self._timer = QTimer()
        self._timer.timeout.connect(self._update_countdown)

    def showEvent(self, event: QShowEvent):
        self._timer.start(1000)
        super().showEvent(event)

    def _update_countdown(self):
        self.timeout -= 1
        if self.timeout == 0:
            self._timer.stop()
            self.defaultButton().animateClick()
        self.setInformativeText(f"Reverting in {self.timeout} Seconds")
