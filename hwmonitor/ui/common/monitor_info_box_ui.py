from PySide2.QtWidgets import QLabel, QFormLayout

from hwmonitor.monitors.monitor import MonitorOrientation
from hwmonitor.ui.ui_util import label_orientation

FMT_DEVICE_NAME = "<b>{}</b>"
FMT_MONITOR_NAME = "<b>{}</b>"
FMT_FRIENDLY_MONITOR_NAME = "<b>{}</b>"
FMT_DISPLAY_ADAPTER = "<b>{}</b>"

FMT_SCREEN_RESOLUTION = "<b>{}x{}</b>"
FMT_VSCREEN_POSITION = "<b>({}, {})</b>"
FMT_MONITOR_ORIENTATION = "<b>{}</b>"
FMT_MONITOR_PRIMARY = "<b>{}</b>"


class UiMonitorInfoBox:

    def __init__(self, view, monitor):
        """ General Infobox for monitor item

        :type view: PySide2.QtWidgets.QWidget.QWidget
        :type monitor: hwmonitor.monitors.monitor.Monitor
        """
        self.monitor = monitor
        self.monitor.property_changed.connect(self._update_property)
        self._layout = QFormLayout()
        self._layout.setRowWrapPolicy(QFormLayout.WrapAllRows)

        self.property_labels = {}
        self.device_name = self._property_label('device_name',
                                                func='device_name', fmt=FMT_DEVICE_NAME, parent=view)
        self.monitor_name = self._property_label('monitor_name',
                                                 func='monitor_name', fmt=FMT_MONITOR_NAME, parent=view)
        self.friendly_monitor_name = self._property_label('friendly_monitor_name',
                                                          func='friendly_monitor_name', fmt=FMT_FRIENDLY_MONITOR_NAME,
                                                          parent=view)
        self.display_adapter = self._property_label('display_adapter',
                                                    func='display_adapter', fmt=FMT_DISPLAY_ADAPTER, parent=view)
        self.screen_resolution = self._property_label('screen_width', 'screen_height',
                                                      func='size', fmt=FMT_SCREEN_RESOLUTION, parent=view)
        self.vscreen_position = self._property_label('position_x', 'position_y',
                                                     func='position', fmt=FMT_VSCREEN_POSITION, parent=view)
        self.orientation = self._property_label('orientation',
                                                func='orientation', fmt=FMT_MONITOR_ORIENTATION, parent=view)
        self.primary = self._property_label('primary',
                                            func='primary', fmt=FMT_MONITOR_PRIMARY, parent=view)

        self._layout.addRow("DEVICE NAME:", self.device_name)
        self._layout.addRow("MONITOR NAME:", self.monitor_name)
        self._layout.addRow("FRIENDLY MONITOR NAME:", self.friendly_monitor_name)
        self._layout.addRow("DISPLAY ADAPTER:", self.display_adapter)
        self._layout.addRow("SCREEN RESOLUTION:", self.screen_resolution)
        self._layout.addRow("VIRTUAL SCREEN POSITION:", self.vscreen_position)
        self._layout.addRow("ORIENTATION:", self.orientation)
        self._layout.addRow("IS PRIMARY:", self.primary)

        view.setLayout(self._layout)

    def _property_label(self, *properties, func='', fmt='', parent=None):
        label = QLabel(parent)

        def wrapped(value=None):
            value = getattr(self.monitor, func)
            if type(value) == tuple:
                text = fmt.format(*value)
            elif isinstance(value, MonitorOrientation):
                text = fmt.format(label_orientation(value))
            else:
                text = fmt.format(value)
            label.setText(text)

        for pro in properties:
            self.property_labels[pro] = wrapped
        wrapped()
        return label

    def _update_property(self, instance, name, value):
        self.property_labels[name]()
