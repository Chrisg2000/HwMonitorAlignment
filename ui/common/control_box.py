from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGroupBox, QHBoxLayout, QFormLayout, QCheckBox, QDialogButtonBox, QAbstractButton


class ControlBox(QGroupBox):

    def __init__(self, controller, parent=None):
        """
        :type controller: align.align_controller.AlignController
        """
        super().__init__(parent)
        self.controller = controller

        self.setTitle("Control Box")
        self._layout = QHBoxLayout()
        self._form_layout = QFormLayout()

        self.show_cursor_position = QCheckBox(self)
        self.show_diagonal_lines = QCheckBox(self)
        self.show_alignment_lines = QCheckBox(self)
        self.show_line_positions = QCheckBox(self)
        self.show_info_box = QCheckBox(self)
        self.show_circles = QCheckBox(self)

        self.show_cursor_position.setChecked(self.controller.show_cursor_position)
        self.show_diagonal_lines.setChecked(self.controller.show_diagonal_lines)
        self.show_alignment_lines.setChecked(self.controller.show_alignment_lines)
        self.show_line_positions.setChecked(self.controller.show_line_positions)
        self.show_info_box.setChecked(self.controller.show_info_box)
        self.show_circles.setChecked(self.controller.show_circles)

        self.show_cursor_position.toggled.connect(self.proxy_property("show_cursor_position"))
        self.show_diagonal_lines.toggled.connect(self.proxy_property("show_diagonal_lines"))
        self.show_alignment_lines.toggled.connect(self.proxy_property("show_alignment_lines"))
        self.show_line_positions.toggled.connect(self.proxy_property("show_line_positions"))
        self.show_info_box.toggled.connect(self.proxy_property("show_info_box"))
        self.show_circles.toggled.connect(self.proxy_property("show_circles"))

        self._form_layout.addRow('Show Cursor Position', self.show_cursor_position)
        self._form_layout.addRow('Show Diagonal Lines', self.show_diagonal_lines)
        self._form_layout.addRow('Show Alignment Lines', self.show_alignment_lines)
        self._form_layout.addRow('Show Line Positions', self.show_line_positions)
        self._form_layout.addRow('Show Info Box', self.show_info_box)
        self._form_layout.addRow('Show Circles', self.show_circles)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Apply |  # Apply Changes to Windows
                                           QDialogButtonBox.Close |  # Close AlignWidget
                                           QDialogButtonBox.Reset,  # Reset model to defaults
                                           Qt.Vertical)
        self.button_box.clicked.connect(self._button_box_clicked)

        self._layout.addLayout(self._form_layout)
        self._layout.addWidget(self.button_box)

        self.setLayout(self._layout)

    def _button_box_clicked(self, button: QAbstractButton):
        if button == self.button_box.button(QDialogButtonBox.Apply):
            pass
        elif button == self.button_box.button(QDialogButtonBox.Close):
            self.controller.stop()
        elif button == self.button_box.button(QDialogButtonBox.Reset):
            pass

    def proxy_property(self, property_name):
        def wrapped(enabled):
            setattr(self.controller, property_name, enabled)

        return wrapped
