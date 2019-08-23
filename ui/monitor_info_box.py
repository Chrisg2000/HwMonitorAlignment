from PySide2.QtWidgets import QGroupBox, QLabel, QFormLayout

from core.monitor import Monitor

LABEL_DEVICE_NAME = "DEVICE NAME:"
FORMAT_DEVICE_NAME = "<b>{}</b>"
LABEL_MONITOR_NAME = "MONITOR NAME:"
FORMAT_MONITOR_NAME = "<b>{}</b>"
LABEL_DISPLAY_MONITOR = "DISPLAY MONITOR:"
FORMAT_DISPLAY_MONITOR = "<b>{}</b>"

LABEL_SCREEN_RESOLUTION = "SCREEN RESOLUTION:"
FORMAT_SCREEN_RESOLUTION = "<b>{}x{}</b>"
LABEL_VSCREEN_POSITION = "VIRTUAL SCREEN POSITION:"
FORMAT_VSCREEN_POSITION = "<b>({}, {})</b>"
LABEL_MONITOR_ORIENTATION = "ORIENTATION:"
FORMAT_MONITOR_ORIENTATION = "<b>{}</b>"
LABEL_MONITOR_PRIMARY = "IS PRIMARY:"
FORMAT_MONITOR_PRIMARY = "<b>{}</b>"


class MonitorInfoBox(QGroupBox):

    def __init__(self, monitor: Monitor, parent=None):
        super().__init__(parent)

        self.monitor = monitor
        self.setTitle("Display Information")
        self._layout = QFormLayout()
        self._layout.setRowWrapPolicy(QFormLayout.WrapAllRows)

        self.device_name = QLabel(self)
        self.monitor_name = QLabel(self)
        self.display_monitor = QLabel(self)
        self.screen_resolution = QLabel(self)
        self.vscreen_position = QLabel(self)
        self.orientation = QLabel(self)
        self.primary = QLabel(self)

        self.device_name.setText(FORMAT_DEVICE_NAME.format(self.monitor.device_name))
        self.monitor_name.setText(FORMAT_MONITOR_NAME.format(self.monitor.monitor_name))
        self.display_monitor.setText(FORMAT_DISPLAY_MONITOR.format(self.monitor.display_monitor))
        self.screen_resolution.setText(FORMAT_SCREEN_RESOLUTION.format(*self.monitor.size))
        self.vscreen_position.setText(FORMAT_VSCREEN_POSITION.format(*self.monitor.position))
        self.orientation.setText(FORMAT_MONITOR_ORIENTATION.format(self.monitor.orientation))
        self.primary.setText(FORMAT_MONITOR_PRIMARY.format(self.monitor.primary))

        self._layout.addRow(LABEL_DEVICE_NAME, self.device_name)
        self._layout.addRow(LABEL_MONITOR_NAME, self.monitor_name)
        self._layout.addRow(LABEL_DISPLAY_MONITOR, self.display_monitor)
        self._layout.addRow(LABEL_SCREEN_RESOLUTION, self.screen_resolution)
        self._layout.addRow(LABEL_VSCREEN_POSITION, self.vscreen_position)
        self._layout.addRow(LABEL_MONITOR_ORIENTATION, self.orientation)
        self._layout.addRow(LABEL_MONITOR_PRIMARY, self.primary)

        self.setLayout(self._layout)
