from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QGridLayout, QLabel, QWidget, QTabWidget, QTableWidget, QDialogButtonBox, qApp

import hwmonitor
from hwmonitor.ui.ui_util import load_pixmap


class AboutDialog(QDialog):
    SOFTWARE_HEADER_NAMES = ['Software', 'License']

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(500, 420)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle('About HwMonitorAlignment')

        self._layout = QGridLayout()
        self._read_libraries()

        self.header_label = QLabel(self)
        self.header_label.setPixmap(load_pixmap('icon.ico').scaled(125, 125, Qt.KeepAspectRatio))
        # self.header_label.setPixmap(QPixmap('doc/hma_logo_left.png').scaledToWidth(480))
        self._layout.addWidget(self.header_label, 0, 0)

        self.short_info = QLabel()
        self.short_info.setAlignment(Qt.AlignCenter)
        self.short_info.setText('<h2>{0} {1}</h2>'
                                '<p>{2}</p>'
                                '<a href="{3}">Project website</a>'
                                .format(str(hwmonitor.__name__),
                                        str(hwmonitor.__version__),
                                        str(hwmonitor.__description__),
                                        str(hwmonitor.__website__)))
        self.short_info.setWordWrap(True)
        self.short_info.setOpenExternalLinks(True)
        self._layout.addWidget(self.short_info, 0, 1)

        # spacer
        self._layout.addWidget(QWidget(), 0, 2, 1, 1)

        # Info tabs
        self.tab_widget = QTabWidget(self)
        self._layout.addWidget(self.tab_widget, 2, 0, 1, 3)

        # Software Licenses Widget
        self.library_table = QTableWidget(len(self._libraries), 2, self.tab_widget)
        self.library_table.setHorizontalHeaderLabels(self.SOFTWARE_HEADER_NAMES)
        self.library_table.horizontalHeader().setStretchLastSection(True)
        self.library_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.library_table.setSelectionMode(QTableWidget.NoSelection)
        self.library_table.verticalHeader().hide()
        self.library_table.setColumnWidth(0, int(self.width() / 3 * 1.8))
        self.library_table.setShowGrid(False)
        self.tab_widget.addTab(self.library_table, 'Third-party software components')

        # Buttons
        self.dialog_buttons = QDialogButtonBox(Qt.Horizontal, self)
        self.dialog_buttons.setStyleSheet('* { button-layout: 2 }')
        self.close_button = self.dialog_buttons.addButton("Close", QDialogButtonBox.AcceptRole)
        self.about_button = self.dialog_buttons.addButton("About Qt", QDialogButtonBox.HelpRole)

        self.close_button.clicked.connect(self.accept)
        self.about_button.clicked.connect(qApp.aboutQt)

        self._layout.addWidget(self.dialog_buttons, 3, 0, 1, 3)

        self._layout.setColumnStretch(0, 1)
        self._layout.setColumnStretch(1, 3)

        self._layout.setRowStretch(0, 6)
        self._layout.setRowStretch(1, 1)
        self._layout.setRowStretch(2, 16)
        self._layout.setRowStretch(3, 3)

        self.setLayout(self._layout)
        self._populate_library_tree()

    def _read_libraries(self):
        """Reads all libraries and licenses from included 'licenses'

        .
        +--library_name
        |  +--version: 0.1
        |  +--license: MIT
        |  +--library_url: http://library.org
        |  +--license_url: http://license.com
        .  .
        """
        import sys
        import PySide2

        self._libraries = {
            'python': {
                'version': '{0}.{1}.{2}-{3}'.format(*sys.version_info),
                'license': 'PSF',
                'library_url': 'http://www.python.org',
                'license_url': 'http://docs.python.org/3/license.html'
            },
            'PySide2': {
                'version': PySide2.__version__,
                'license': 'GNU LGPL v3',
                'library_url': 'http://www.qt.io/qt-for-python',
                'license_url': 'https://doc.qt.io/qt-5/lgpl.html'
            },
            'Components of linux-show-player': {
                'version': '',
                'license': 'GNU GPL v3',
                'library_url': 'https://github.com/FrancescoCeruti/linux-show-player',
                'license_url': 'https://github.com/FrancescoCeruti/linux-show-player/blob/master/LICENSE'
            }
        }

    def _populate_library_tree(self):
        """Puts every library name and license into model for library view
        """
        for i, library in enumerate(self._libraries):
            library_info = self._libraries[library]

            library_text = '<a href="{0}">{1}</a> <font color="#777">{2}</font>'.format(library_info['library_url'],
                                                                                        library,
                                                                                        library_info['version'])
            license_text = '<a href="{0}">{1}</a>'.format(library_info['license_url'],
                                                          library_info['license'])

            name_label, license_label = self._library_item_widgets(library_text, license_text)

            self.library_table.setCellWidget(i, 0, name_label)
            self.library_table.setCellWidget(i, 1, license_label)

    @staticmethod
    def _library_item_widgets(library_text, license_text):
        name_label = QLabel()
        name_label.setText(library_text)
        name_label.setTextFormat(Qt.RichText)
        name_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        name_label.setOpenExternalLinks(True)
        name_label.setMargin(5)

        license_label = QLabel()
        license_label.setText(license_text)
        license_label.setTextFormat(Qt.RichText)
        license_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        license_label.setOpenExternalLinks(True)

        return name_label, license_label
