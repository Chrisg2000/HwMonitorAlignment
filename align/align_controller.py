from PySide2.QtCore import Qt

from backend.monitor_backend import BaseMonitorBackend
from ui.align.align_widget import AlignWidget


class AlignController:

    def __init__(self, backend: BaseMonitorBackend):
        self.backend = backend
        self.active = False

        self.backend.monitor_added.connect(self._monitor_model_changed)
        self.backend.monitor_removed.connect(self._monitor_model_changed)
        self.backend.monitor_model_reset.connect(self._monitor_model_changed)

        self._widget = AlignWidget(self)

    def start(self):
        self._widget.show()
        self.active = True

    def stop(self, force=False):
        self._widget.close()
        self.active = False

    def get_monitor(self, index):
        return self.backend.monitor_model.get(index)

    def key_pressed(self, key, instance):
        if key == Qt.Key_Escape:
            self.stop()

    def _monitor_model_changed(self, *args):
        if self.active:
            self.stop(True)
            self.start()
