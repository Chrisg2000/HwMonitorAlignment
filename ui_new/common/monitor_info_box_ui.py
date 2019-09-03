from PySide2.QtWidgets import QLabel, QFormLayout

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


def format_proxy(fmt: str, orientation=False):
    def wrapped(value):
        if type(value) == tuple:
            return fmt.format(*value)
        if orientation:
            value = label_orientation(value)
        return fmt.format(value)

    return wrapped


class UiMonitorInfoBox:

    def __init__(self, view, monitor):
        """ General Infobox for monitor item

        :type view: PySide2.QtWidgets.QWidget.QWidget
        :type monitor: monitors.monitor.Monitor
        """

        self.monitor = monitor
        self.monitor.property_changed.connect(self._update_property)
        self._layout = QFormLayout()
        self._layout.setRowWrapPolicy(QFormLayout.WrapAllRows)

        self.device_name = QLabel(view)
        self.monitor_name = QLabel(view)
        self.display_monitor = QLabel(view)
        self.screen_resolution = QLabel(view)
        self.vscreen_position = QLabel(view)
        self.orientation = QLabel(view)
        self.primary = QLabel(view)

        self.mapper = {
            'device_name': ('device_name', format_proxy(FMT_DEVICE_NAME), self.device_name),
            'monitor_name': ('monitor_name', format_proxy(FMT_MONITOR_NAME), self.monitor_name),
            'display_monitor': ('display_monitor', format_proxy(FMT_DISPLAY_MONITOR), self.display_monitor),
            'screen_width': ('size', format_proxy(FMT_SCREEN_RESOLUTION), self.screen_resolution),
            'screen_height': ('size', format_proxy(FMT_SCREEN_RESOLUTION), self.screen_resolution),
            'position_x': ('position', format_proxy(FMT_VSCREEN_POSITION), self.vscreen_position),
            'position_y': ('position', format_proxy(FMT_VSCREEN_POSITION), self.vscreen_position),
            'orientation': ('orientation', format_proxy(FMT_MONITOR_ORIENTATION, orientation=True), self.orientation),
            'primary': ('primary', format_proxy(FMT_MONITOR_PRIMARY), self.primary),
        }

        for (attr, fmt, label) in self.mapper.values():
            label.setText(fmt(getattr(self.monitor, attr)))

        self._layout.addRow("DEVICE NAME:", self.device_name)
        self._layout.addRow("MONITOR NAME:", self.monitor_name)
        self._layout.addRow("DISPLAY MONITOR:", self.display_monitor)
        self._layout.addRow("SCREEN RESOLUTION:", self.screen_resolution)
        self._layout.addRow("VIRTUAL SCREEN POSITION:", self.vscreen_position)
        self._layout.addRow("ORIENTATION:", self.orientation)
        self._layout.addRow("IS PRIMARY:", self.primary)

        view.setLayout(self._layout)

    def _update_property(self, instance, name, value):
        attr, fmt, label = self.mapper[name]
        label.setText(fmt(getattr(self.monitor, attr)))
