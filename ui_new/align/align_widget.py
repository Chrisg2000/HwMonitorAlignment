from PySide2.QtWidgets import QGraphicsView

from ui_new.align.align_widget_ui import UiAlignWidget


class AlignWidget(QGraphicsView):

    def __init__(self, controller, model, monitor, parent=None):
        """Widget which is drawn on every monitor to align them.

        The model and controller is shared among all other widgets on the different monitors

        :type controller: ui_new.align.align_controller.AlignController
        :type model: ui_new.align.align_widget_model.AlignWidgetModel
        :type monitor: monitors.monitor.Monitor
        """
        super().__init__(parent)
        self.model = model
        self.monitor = monitor
        self.controller = controller

        self.ui = UiAlignWidget(self, self.model, self.monitor)

        self.move(self.monitor.position_x,
                  self.monitor.position_y)
        self.resize(self.monitor.screen_width,
                    self.monitor.screen_height)
