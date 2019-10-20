from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGraphicsProxyWidget


class GraphicsWindow(QGraphicsProxyWidget):

    def __init__(self, widget, title='', flags=0, parent=None):
        """ Embed widget inside an OS-provided window inside a GraphicsView.

        :type widget: PySide2.QtWidgets.QWidget.QWidget
        """
        self.title = title
        self.widget = widget
        self.flags = (flags |
                      Qt.Dialog |
                      Qt.WindowTitleHint |
                      Qt.CustomizeWindowHint)
        super().__init__(parent, self.flags)

        self.setWidget(self.widget)
        self.setWindowTitle(self.title)
        self.setMaximumSize(widget.sizeHint())
        self.setMinimumSize(widget.sizeHint())
