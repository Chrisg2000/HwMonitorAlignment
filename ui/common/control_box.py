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

        self.show_cursor_position = self._property_checkbox("show_cursor_position", self)
        self.show_diagonal_lines = self._property_checkbox("show_diagonal_lines", self)
        self.show_alignment_lines = self._property_checkbox("show_alignment_lines", self)
        self.show_line_positions = self._property_checkbox("show_line_positions", self)
        self.show_info_box = self._property_checkbox("show_info_box", self)
        self.show_circles = self._property_checkbox("show_circles", self)

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

    def _property_checkbox(self, property_name: str, parent=None):
        def wrapped(enabled):
            setattr(self.controller, property_name, enabled)

        check_box = QCheckBox(parent)
        check_box.setChecked(getattr(self.controller, property_name))
        check_box.toggled.connect(wrapped)
        return check_box
