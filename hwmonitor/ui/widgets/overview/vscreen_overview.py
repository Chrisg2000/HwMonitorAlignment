from PySide2.QtCore import QSize
from PySide2.QtGui import QResizeEvent
from PySide2.QtWidgets import QGraphicsView

from hwmonitor.ui.widgets.overview.vscreen_overview_ui import UiVScreenOverview
from hwmonitor.vscreen.vscreen import VScreen


class VScreenOverview(QGraphicsView):

    def __init__(self, vscreen: VScreen, parent=None):
        super().__init__(parent=parent)
        self.vscreen = vscreen
        self.ui = UiVScreenOverview(self, vscreen)

        self.vscreen.layout_changed.connect(self._update_view)

    def sizeHint(self) -> QSize:
        return QSize()

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, width: int) -> int:
        view_rect = self.viewport().rect()
        ratio = view_rect.height() / view_rect.width()
        return int(width * ratio)

    def resizeEvent(self, event: QResizeEvent):
        self.ui.resize_scene()
        super().resizeEvent(event)

    def _update_view(self):
        self.ui.resize_scene()
