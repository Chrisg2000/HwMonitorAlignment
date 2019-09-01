from PySide2.QtWidgets import QGroupBox, QLabel, QFormLayout

from monitors.monitor import DisplayOrientation

FMT_DEVICE_NAME = "<b>{}</b>"
FMT_MONITOR_NAME = "<b>{}</b>"
FMT_DISPLAY_MONITOR = "<b>{}</b>"

FMT_SCREEN_RESOLUTION = "<b>{}x{}</b>"
FMT_VSCREEN_POSITION = "<b>({}, {})</b>"
FMT_MONITOR_ORIENTATION = "<b>{}</b>"
FMT_MONITOR_PRIMARY = "<b>{}</b>"


def label_orientation(orientation: DisplayOrientation):
    if orientation == DisplayOrientation.DMDO_DEFAULT:
        return 'Landscape'
    elif orientation == DisplayOrientation.DMDO_90:
        return 'Portrait'
    elif orientation == DisplayOrientation.DMDO_180:
        return 'Landscape (flipped)'
    elif orientation == DisplayOrientation.DMDO_270:
        return 'Portrait (flipped)'
    else:
        raise ValueError("orientation needs to be a DisplayOrientation")


class UiMonitorInfoBox:

    def __init__(self, view, monitor):
        """ General Infobox for monitor item

        :type view: PySide2.QtWidgets.QWidget.QWidget
        :type monitor: monitors.monitor.Monitor
        """

        self.monitor = monitor
        self._layout = QFormLayout()
        self._layout.setRowWrapPolicy(QFormLayout.WrapAllRows)

        self.device_name = self._property_label(('device_name',), 'device_name', FMT_DEVICE_NAME, view)
        self.monitor_name = self._property_label(('monitor_name',), 'monitor_name', FMT_MONITOR_NAME, view)
        self.display_monitor = self._property_label(('display_monitor',), 'display_monitor', FMT_DISPLAY_MONITOR, view)
        self.screen_resolution = self._property_label(('screen_width', 'screen_height')
                                                      , 'size', FMT_SCREEN_RESOLUTION, view)
        self.vscreen_position = self._property_label(('position_x', 'position_y'),
                                                     'position', FMT_VSCREEN_POSITION, view)
        self.orientation = self._property_label(('orientation',), 'orientation', FMT_MONITOR_ORIENTATION, view, True)
        self.primary = self._property_label(('primary',), 'primary', FMT_MONITOR_PRIMARY, view)

        self._layout.addRow("DEVICE NAME:", self.device_name)
        self._layout.addRow("MONITOR NAME:", self.monitor_name)
        self._layout.addRow("DISPLAY MONITOR:", self.display_monitor)
        self._layout.addRow("SCREEN RESOLUTION:", self.screen_resolution)
        self._layout.addRow("VIRTUAL SCREEN POSITION:", self.vscreen_position)
        self._layout.addRow("ORIENTATION:", self.orientation)
        self._layout.addRow("IS PRIMARY:", self.primary)

        view.setLayout(self._layout)

    def _property_label(self, property_name, func, fmt, parent=None, orientation=False):
        """
        :param tuple property_name: Container of property names in monitor model
        :param str func: Name of property to use to display
        :param str fmt: Format string for property
        :param parent: QLabel parent
        :param orientation: Is Label for orientation
        """
        label = QLabel(parent)

        def wrapped(value):
            attr = getattr(self.monitor, func)
            if type(attr) == tuple:
                text = fmt.format(*attr)
            elif orientation:
                text = fmt.format(label_orientation(attr))
            else:
                text = fmt.format(attr)
            label.setText(text)

        for name in property_name:
            self.monitor.changed(name).connect(wrapped)
        wrapped(None)
        return label
