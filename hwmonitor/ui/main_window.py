from PySide2.QtWidgets import QMainWindow

from hwmonitor.ui.main_window_ui import UiMainWindow
from hwmonitor.ui.widgets.align.align_controller import AlignController
from hwmonitor.vscreen.vscreen import VScreen


class MainWindow(QMainWindow):

    def __init__(self, vscreen: VScreen):
        super().__init__()
        self.vscreen = vscreen
        self.align_controller = AlignController(self.vscreen)

        self.ui = UiMainWindow(self, self.vscreen)
        self.ui.close_button.clicked.connect(self._button_close)
        self.ui.adjust_button.clicked.connect(self._button_adjust)
        self.ui.about_button.clicked.connect(self._button_about)

    def _button_close(self, checked=False):
        self.close()

    def _button_adjust(self, checked=False):
        self.align_controller.start()

    def _button_about(self, checked=False):
        from hwmonitor.ui.dialogs.about_dialog import AboutDialog
        AboutDialog(self).show()

    def finalize(self):
        self.align_controller.stop()
