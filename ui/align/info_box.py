from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGraphicsItem, QGraphicsWidget, \
    QGraphicsLinearLayout, QLabel, QGraphicsProxyWidget, QGroupBox, QVBoxLayout

from core.monitor import Monitor

TEXT_DEVICE_NAME = "DEVICE NAME:<br><b>{}</b>"
TEXT_MONITOR_NAME = "MONITOR NAME:<br><b>{}</b>"
TEXT_DISPLAY_MONITOR = "DISPLAY MONITOR:<br><b>{}</b>"
TEXT_SCREEN_RESOLUTION = "SCREEN RESOLUTION:<br><b>{}x{}</b>"
TEXT_VSCREEN_POSITION = "VIRTUAL SCREEN POSITION:<br><b>({}, {})</b>"
TEXT_MONITOR_ORIENTATION = "ORIENTATION:<br><b>{}</b>"
TEXT_MONITOR_PRIMARY = "IS PRIMARY:<br><b>{}</b>"


class InfoBox(QGraphicsWidget):

    def __init__(self, monitor: Monitor):
        super().__init__()
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemSendsScenePositionChanges)
        self.monitor = monitor

        self._layout = QGraphicsLinearLayout(Qt.Vertical)
        self.setLayout(self._layout)

        self._group_box = QGroupBox('Display Information')
        self._group_box_layout = QVBoxLayout()
        self._group_box.setLayout(self._group_box_layout)

        self.device_name = QLabel(self._group_box)
        self.monitor_name = QLabel(self._group_box)
        self.display_monitor = QLabel(self._group_box)
        self.screen_resolution = QLabel(self._group_box)
        self.vscreen_position = QLabel(self._group_box)
        self.orientation = QLabel(self._group_box)
        self.primary = QLabel(self._group_box)

        self._group_box_layout.addWidget(self.device_name)
        self._group_box_layout.addWidget(self.monitor_name)
        self._group_box_layout.addWidget(self.display_monitor)
        self._group_box_layout.addWidget(self.screen_resolution)
        self._group_box_layout.addWidget(self.vscreen_position)
        self._group_box_layout.addWidget(self.orientation)
        self._group_box_layout.addWidget(self.primary)

        self.widget_group_box = QGraphicsProxyWidget()
        self.widget_group_box.setWidget(self._group_box)

        self._layout.addItem(self.widget_group_box)

        self.device_name.setText(
            TEXT_DEVICE_NAME.format(self.monitor.device_name))
        self.monitor_name.setText(
            TEXT_MONITOR_NAME.format(self.monitor.monitor_name))
        self.display_monitor.setText(
            TEXT_DISPLAY_MONITOR.format(self.monitor.display_monitor))
        self.screen_resolution.setText(
            TEXT_SCREEN_RESOLUTION.format(self.monitor.screen_width, self.monitor.screen_height))
        self.vscreen_position.setText(
            TEXT_VSCREEN_POSITION.format(self.monitor.position_x, self.monitor.position_y))
        self.orientation.setText(
            TEXT_MONITOR_ORIENTATION.format(self.monitor.orientation))
        self.primary.setText(
            TEXT_MONITOR_PRIMARY.format(self.monitor.primary))

        monitor.property_changed.connect(self._property_changed)

    def _property_changed(self, instance, name, value):
        if name is 'device_name':
            self.device_name.setText(TEXT_DEVICE_NAME.format(self.monitor.device_name))
        elif name is 'monitor_name':
            self.monitor_name.setText(TEXT_MONITOR_NAME.format(self.monitor.monitor_name))
        elif name is 'screen_width' or name is 'screen_height':
            self.screen_resolution.setText(
                TEXT_SCREEN_RESOLUTION.format(self.monitor.screen_width, self.monitor.screen_height))
        elif name is 'position_x' or name is 'position_y':
            self.position.setText(
                TEXT_VSCREEN_POSITION.format(self.monitor.position_x, self.monitor.position_y))
        elif name is 'orientation':
            self.orientation.setText(TEXT_MONITOR_ORIENTATION.format(self.monitor.orientation))
        elif name is 'primary':
            self.primary.setText(TEXT_MONITOR_PRIMARY.format(self.monitor.primary))
