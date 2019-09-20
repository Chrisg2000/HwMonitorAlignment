from hwmonitor.ui.main_window import MainWindow
from hwmonitor.module.win32_backend.win32_backend import Win32Backend


class HwMonitorAlignmentApp:

    def __init__(self):
        self.backend = Win32Backend()
        self.vscreen = self.backend.get_vscreen()
        self.main_window = None

    def start(self):
        self.main_window = MainWindow(self.vscreen)
        self.main_window.show()

    def finalize(self, exit_code: int):
        self.backend.finalize(exit_code)
        self.main_window.finalize()
