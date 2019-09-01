from backend.monitor_backend import BaseMonitorBackend
from core.has_properties import HasProperties, Property


class AlignWidgetModel(HasProperties):
    show_diagonal_lines = Property(default=False)
    show_horizontal_lines = Property(default=True)
    show_info_box = Property(default=True)
    line_spacing = Property(default=100)
    line_thickness = Property(default=3.0)

    def __init__(self, backend: BaseMonitorBackend):
        super().__init__()
        self.backend = backend

    @property
    def vscreen_offset(self):
        return self.backend.get_vscreen_normalize_offset()

    @property
    def vscreen_size(self):
        return self.backend.get_vscreen_size()
