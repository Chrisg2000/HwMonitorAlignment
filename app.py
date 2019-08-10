from backend.win32_backend import Win32Backend
from ui.main_window import MainWindow


class HwMonitorAlignmentApp:

    def __init__(self):
        self.backend = Win32Backend()
        self.main_window = MainWindow(self.backend)

    def start(self):
        self.main_window.show()

    def finalize(self, exit_code: int):
        pass
