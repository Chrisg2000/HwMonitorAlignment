from PySide2.QtCore import Qt
from PySide2.QtGui import QMouseEvent
from PySide2.QtWidgets import QToolTip

from hwmonitor.ui.align.align_widget import AlignWidget
from hwmonitor.ui.align.models.align_model import AlignModel
from hwmonitor.ui.align.models.view_model import AlignViewModel
from hwmonitor.ui.dialogs.settings_changed import DisplaySettingsChanged


class AlignController:

    def __init__(self, monitor_model_adapter):
        """Controller for the widgets on the different monitors.

        The internal model and controller is shared among all other
        widgets on the different monitors

                                Controller
            ┌─────────────   modifies models    <────────────┐
            │             and common properties              │ common
         ViewModel         │                                 │ properties
        common UI  ───┐    │                                 │ change
        properties    │    │                                 │ or general
                      ├──> ├────>   Model  ────────>  View ──┤ settings
                      │    │                                 │
                      ├──> ├────>   Model  ────────>  View ──┤
                      │    │                                 │
                      └──> └────>   Model  ────────>  View ──┘
                                 specific UI        displays
                                properties and      specific
                                     data            data


        :type monitor_model_adapter: hwmonitor.monitors.vscreen_adapter.VScreenAdapter
        """
        self.map = {}
        self.monitor_model_adapter = monitor_model_adapter
        self.common_model = AlignViewModel()

    def key_pressed(self, model: AlignModel, key):
        if key == Qt.Key_Escape:
            self.stop()
        elif key == Qt.Key_Up and not model.monitor.primary:
            model.offset -= 1
        elif key == Qt.Key_Down and not model.monitor.primary:
            model.offset += 1
        else:
            return True

    def wheel_event(self, model, event):
        return False

    def mouse_move_event(self, model, event: QMouseEvent):
        if self.common_model.show_cursor_position:
            QToolTip.showText(event.globalPos(),
                              f"{event.globalPos().x()}, {event.globalPos().y()}")
        return True

    def start(self):
        for monitor in self.monitor_model_adapter:
            model = AlignModel(monitor, self.common_model, self.monitor_model_adapter)
            widget = AlignWidget(self, model)
            widget.showFullScreen()

            self.map[monitor] = (model, widget)

    def stop(self):
        for _, widget in self.map.values():
            widget.close()
        self.map.clear()

    def button_apply(self, checked=False):
        """Align Widget Control Box Dialog Buttons Apply"""
        for model, _ in self.map.values():
            model.apply_offset()

        # Reset logic
        dialog = DisplaySettingsChanged(timeout=20)
        rst = dialog.exec_()
        if rst == DisplaySettingsChanged.No:
            for model, _ in self.map.values():
                model.rollback()
                model.apply_offset()

    def button_close(self, checked=False):
        """Align Widget Control Box Dialog Buttons Close"""
        self.stop()

    def button_reset(self, checked=False):
        """Align Widget Control Box Dialog Buttons Reset"""
        for model, _ in self.map.values():
            model.rollback()
