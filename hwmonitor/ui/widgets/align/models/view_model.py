from hwmonitor.core.has_properties import HasProperties, Property


class AlignViewModel(HasProperties):
    show_cursor_position = Property(default=False)
    show_diagonal_lines = Property(default=False)
    show_horizontal_lines = Property(default=True)
    antialiasing = Property(default=False)
    show_info_box = Property(default=True)
    line_spacing = Property(default=100)
    line_thickness = Property(default=3.0)
