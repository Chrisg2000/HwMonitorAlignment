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

    def __init__(self, view, monitor, model=None):
        """ General Infobox for monitor item

        :type view: PySide2.QtWidgets.QWidget.QWidget
        :type monitor: monitors.monitor.Monitor
        :type model: ui_new.align.models.align_model.AlignModel
        """
        self.monitor = monitor
        self.monitor.property_changed.connect(self._update_property)
        self.model = model
        self._layout = QFormLayout()
        self._layout.setRowWrapPolicy(QFormLayout.WrapAllRows)

        self.property_labels = {}
        self.device_name = self._property_label('device_name', func='device_name',
                                                fmt=FMT_DEVICE_NAME, parent=view)
        self.monitor_name = self._property_label('monitor_name', func='monitor_name',
                                                 fmt=FMT_MONITOR_NAME, parent=view)
        self.display_monitor = self._property_label('display_monitor', func='display_monitor',
                                                    fmt=FMT_DISPLAY_MONITOR, parent=view)
        self.screen_resolution = self._property_label('screen_width', 'screen_height', func='size',
                                                      fmt=FMT_SCREEN_RESOLUTION, parent=view)
        self.vscreen_position = self._property_label('position_x', 'position_y', func='position',
                                                     fmt=FMT_VSCREEN_POSITION, parent=view, model_prop='offset',
                                                     model_func=self._position_model_modification)
        self.orientation = self._property_label('orientation', func='orientation',
                                                fmt=FMT_MONITOR_ORIENTATION, parent=view, ori=True)
        self.primary = self._property_label('primary', func='primary',
                                            fmt=FMT_MONITOR_PRIMARY, parent=view)

        self._layout.addRow("DEVICE NAME:", self.device_name)
        self._layout.addRow("MONITOR NAME:", self.monitor_name)
        self._layout.addRow("DISPLAY MONITOR:", self.display_monitor)
        self._layout.addRow("SCREEN RESOLUTION:", self.screen_resolution)
        self._layout.addRow("VIRTUAL SCREEN POSITION:", self.vscreen_position)
        self._layout.addRow("ORIENTATION:", self.orientation)
        self._layout.addRow("IS PRIMARY:", self.primary)

        view.setLayout(self._layout)

    def _property_label(self, *properties, func='', fmt='', parent=None, ori=False, model_prop='', model_func=None):
        label = QLabel(parent)

        def wrapped(value=None):
            value = getattr(self.monitor, func)
            if model_prop and self.model:
                value = model_func(value)
            if type(value) == tuple:
                text = fmt.format(*value)
            elif ori:
                text = fmt.format(label_orientation(value))
            else:
                text = fmt.format(value)
            label.setText(text)

        for pro in properties:
            self.property_labels[pro] = wrapped
        if model_prop and self.model:
            self.model.changed(model_prop).connect(wrapped)
        wrapped()
        return label

    def _update_property(self, instance, name, value):
        self.property_labels[name]()

    def _position_model_modification(self, value):
        x, y = value
        y += self.model.offset
        return x, y
