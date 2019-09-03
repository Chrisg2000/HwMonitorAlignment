from core.has_properties import HasProperties, Property


class AlignViewModel(HasProperties):
    show_diagonal_lines = Property(default=False)
    show_horizontal_lines = Property(default=True)
    show_info_box = Property(default=True)
    line_spacing = Property(default=100)
    line_thickness = Property(default=3.0)
