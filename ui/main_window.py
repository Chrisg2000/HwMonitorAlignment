from PySide2.QtCore import QRect, Qt
from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMenuBar, QMenu, QAction

from backend.backend import Backend
from core.monitor_model import MonitorModel
from ui.widgets.measured_monitor_overview import MeasuredMonitorOverview
from ui.widgets.monitor_overview import MonitorOverview


class MainWindow(QMainWindow):

    def __init__(self, backend: Backend):
        super().__init__()
        # self.resize(1280, 720)
        self.resize(492, 219)
        # self.setMinimumSize(1280, 720)
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(QVBoxLayout())
        # self.centralWidget().layout().setContentsMargins(5, 5, 5, 5)
        self.centralWidget().layout().setContentsMargins(0, 0, 0, 0)

        self.backend = backend

        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 0, 25))
        self.menubar.setContextMenuPolicy(Qt.PreventContextMenu)

        self.menu_debug = QMenu(self.menubar)
        self.menu_debug.setTitle('Debug')

        # menuDebug
        self.actionNewMonitor = QAction(self)
        self.actionNewMonitor.triggered.connect(self.__new_monitor)
        self.actionNewMonitor.setText('Add Monitor')

        self.actionRemoveMonitor = QAction(self)
        self.actionNewMonitor.triggered.connect(self.__remove_monitor)
        self.actionRemoveMonitor.setText('Remove Monitor')

        self.actionResetModel = QAction(self)
        self.actionNewMonitor.triggered.connect(self.__reset_model)
        self.actionResetModel.setText('Reset Model')

        self.menu_debug.addAction(self.actionNewMonitor)
        self.menu_debug.addAction(self.actionRemoveMonitor)
        self.menu_debug.addAction(self.actionResetModel)
        self.menubar.addMenu(self.menu_debug)
        self.setMenuBar(self.menubar)

        widget = MonitorOverview(self.backend)
        self.centralWidget().layout().addWidget(widget)

        # widget2 = MeasuredMonitorOverview(self.backend)
        # self.centralWidget().layout().addWidget(widget2)

    def __new_monitor(self):
        item = MonitorModel()
        item.device_name = r'\\.\DISPLAY4'
        item.monitor_name = 'Debug-Monitor'
        item.screen_width = 1920
        item.screen_height = 1080
        item.position_x = 0
        item.position_y = -1080
        self.backend.monitor_model.add(item)

    def __remove_monitor(self):
        pass

    def __reset_model(self):
        pass
