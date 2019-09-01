from PySide2.QtWidgets import QWidget

from ui_new.common.control_box_ui import UiControlBox
from ui_new.graphics.graphics_window import GraphicsWindow


class ControlBoxItem(GraphicsWindow):

    def __init__(self, model, parent=None):
        self.model = model
        self.widget = QWidget()
        self.ui = UiControlBox(self.widget, self.model)

        super().__init__(self.widget, 'Control Box', 0, parent)
