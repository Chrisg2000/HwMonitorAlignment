from PySide2.QtGui import QKeyEvent, QWheelEvent, QMouseEvent
from PySide2.QtWidgets import QGraphicsView, QDialogButtonBox

from hwmonitor.ui.align.align_widget_ui import UiAlignWidget


class AlignWidget(QGraphicsView):

    def __init__(self, controller, model, parent=None):
        """Widget which is drawn on every monitor to align them.

        The model and controller is shared among all other widgets on the different _monitors

        :type controller: hwmonitor.ui.align.align_controller.AlignController
        :type model: hwmonitor.ui.align.models.align_model.AlignModel
        """
        super().__init__(parent)
        self.model = model
        self.controller = controller

        self.ui = UiAlignWidget(self, self.model)
        if self.model.monitor.primary:
            # Control Box Buttons
            self.ui.control_box.ui.button_box.button(QDialogButtonBox.Apply).clicked.connect(
                self.controller.button_apply)
            self.ui.control_box.ui.button_box.button(QDialogButtonBox.Close).clicked.connect(
                self.controller.button_close)
            self.ui.control_box.ui.button_box.button(QDialogButtonBox.Reset).clicked.connect(
                self.controller.button_reset)

        self.move(self.model.monitor.position_x,
                  self.model.monitor.position_y)
        self.resize(self.model.monitor.screen_width,
                    self.model.monitor.screen_height)

    def keyPressEvent(self, event: QKeyEvent):
        if self.controller.key_pressed(self.model, event.key()):
            super().keyPressEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        if self.controller.wheel_event(self.model, event):
            super().wheelEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.controller.mouse_move_event(self.model, event):
            super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        self.ui.info_box.widget.raise_()
        super().mousePressEvent(event)
