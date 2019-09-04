from PySide2.QtWidgets import QWidget

from ui_new.common.monitor_info_box_ui import UiMonitorInfoBox
from ui_new.graphics.graphics_window import GraphicsWindow


class MonitorInfoBoxItem(GraphicsWindow):

    def __init__(self, model, text='Display Information', parent=None):
        self.model = model
        self.widget = QWidget()
        self.ui = UiMonitorInfoBox(self.widget, monitor=self.model.monitor, model=self.model)

        super().__init__(self.widget, text, 0, parent)
