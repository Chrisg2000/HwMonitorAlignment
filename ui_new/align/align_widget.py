from PySide2.QtGui import QKeyEvent, QWheelEvent
from PySide2.QtWidgets import QGraphicsView, QDialogButtonBox

from ui_new.align.align_widget_ui import UiAlignWidget


class AlignWidget(QGraphicsView):

    def __init__(self, controller, model, monitor, parent=None):
        """Widget which is drawn on every monitor to align them.

        The model and controller is shared among all other widgets on the different monitors

        :type controller: ui_new.align.align_controller.AlignController
        :type model: ui_new.align.align_widget_model.AlignWidgetViewModel
        :type monitor: monitors.monitor.Monitor
        """
        super().__init__(parent)
        self.model = model
        self.monitor = monitor
        self.controller = controller

        self.ui = UiAlignWidget(self, self.model, self.monitor)
        if self.monitor.primary:
            # Control Box Buttons
            self.ui.control_box.ui.button_box.button(QDialogButtonBox.Apply).clicked.connect(
                self.controller.button_apply)
            self.ui.control_box.ui.button_box.button(QDialogButtonBox.Close).clicked.connect(
                self.controller.button_close)
            self.ui.control_box.ui.button_box.button(QDialogButtonBox.Reset).clicked.connect(
                self.controller.button_reset)

        self.move(self.monitor.position_x,
                  self.monitor.position_y)
        self.resize(self.monitor.screen_width,
                    self.monitor.screen_height)

    def keyPressEvent(self, event: QKeyEvent):
        if self.controller.key_pressed(self.monitor, event.key()):
            super().keyPressEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        self.controller.wheel_event(self.monitor, event)
