from PySide2.QtWidgets import QGroupBox, QLabel, QFormLayout

from monitors.monitor import Monitor, DisplayOrientation

LABEL_DEVICE_NAME = "DEVICE NAME:"
FMT_DEVICE_NAME = "<b>{}</b>"
LABEL_MONITOR_NAME = "MONITOR NAME:"
FMT_MONITOR_NAME = "<b>{}</b>"
LABEL_DISPLAY_MONITOR = "DISPLAY MONITOR:"
FMT_DISPLAY_MONITOR = "<b>{}</b>"

LABEL_SCREEN_RESOLUTION = "SCREEN RESOLUTION:"
FMT_SCREEN_RESOLUTION = "<b>{}x{}</b>"
LABEL_VSCREEN_POSITION = "VIRTUAL SCREEN POSITION:"
FMT_VSCREEN_POSITION = "<b>({}, {})</b>"
LABEL_MONITOR_ORIENTATION = "ORIENTATION:"
FMT_MONITOR_ORIENTATION = "<b>{}</b>"
LABEL_MONITOR_PRIMARY = "IS PRIMARY:"
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


class MonitorInfoBox(QGroupBox):

    def __init__(self, monitor: Monitor, parent=None):
        super().__init__(parent)

        self.monitor = monitor
        self.monitor.property_changed.connect(self._update_property)
        self._selected = False
        self.setTitle(f"Display Information {'*' if self._selected else ''}")
        self._layout = QFormLayout()
        self._layout.setRowWrapPolicy(QFormLayout.WrapAllRows)

        self.device_name = QLabel(self)
        self.monitor_name = QLabel(self)
        self.display_monitor = QLabel(self)
        self.screen_resolution = QLabel(self)
        self.vscreen_position = QLabel(self)
        self.orientation = QLabel(self)
        self.primary = QLabel(self)

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

        self._layout.addRow(LABEL_DEVICE_NAME, self.device_name)
        self._layout.addRow(LABEL_MONITOR_NAME, self.monitor_name)
        self._layout.addRow(LABEL_DISPLAY_MONITOR, self.display_monitor)
        self._layout.addRow(LABEL_SCREEN_RESOLUTION, self.screen_resolution)
        self._layout.addRow(LABEL_VSCREEN_POSITION, self.vscreen_position)
        self._layout.addRow(LABEL_MONITOR_ORIENTATION, self.orientation)
        self._layout.addRow(LABEL_MONITOR_PRIMARY, self.primary)

        self.setLayout(self._layout)

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
        self.setTitle(f"Display Information {'*' if self.selected else ''}")

    def _update_property(self, instance, name, value):
        attr, fmt, label = self.mapper[name]
        label.setText(fmt(getattr(self.monitor, attr)))
