from PySide2.QtCore import Qt
from PySide2.QtWidgets import QHBoxLayout, QFormLayout, QCheckBox, QDialogButtonBox, QSpinBox


class UiControlBox:

    def __init__(self, view, model):
        """Align Widget Control Box Ui

        :type view: PySide2.QtWidgets.QWidget.QWidget
        :type model: ui_new.align.models.view_model.AlignViewModel
        """
        self.model = model
        self._layout = QHBoxLayout()
        self._form_layout = QFormLayout()

        self.show_diagonal_lines = self._property_checkbox("show_diagonal_lines", view)
        self.show_horizontal_lines = self._property_checkbox("show_horizontal_lines", view)
        self.line_spacing = self._property_spinbox("line_spacing", (50, 1920 // 2), view)
        self.line_thickness = self._property_spinbox("line_thickness", (0, 100), view)
        self.show_info_box = self._property_checkbox("show_info_box", view)

        self._form_layout.addRow("Show diagonal lines", self.show_diagonal_lines)
        self._form_layout.addRow("Show horizontal lines", self.show_horizontal_lines)
        self._form_layout.addRow("Line spacing", self.line_spacing)
        self._form_layout.addRow("Line thickness", self.line_thickness)
        self._form_layout.addRow("Show info box", self.show_info_box)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Apply |  # Commit changes to windows
                                           QDialogButtonBox.Close |  # Close AlignWidget
                                           QDialogButtonBox.Reset,  # Reset changes
                                           Qt.Vertical)

        self._layout.addLayout(self._form_layout)
        self._layout.addWidget(self.button_box)

        view.setLayout(self._layout)

    def _property_checkbox(self, property_name, parent=None):
        def wrapped(enabled):
            setattr(self.model, property_name, enabled)

        check_box = QCheckBox(parent)
        check_box.setChecked(getattr(self.model, property_name))
        check_box.toggled.connect(wrapped)
        return check_box

    def _property_spinbox(self, property_name, range_=(0, 99), parent=None):
        def wrapped(value: int):
            if type(value) == str:
                return
            setattr(self.model, property_name, value)

        spin_box = QSpinBox(parent)
        spin_box.setRange(*range_)
        spin_box.setValue(getattr(self.model, property_name))
        spin_box.valueChanged.connect(wrapped)
        return spin_box
