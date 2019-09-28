import sys

from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication

from hwmonitor.app import HwMonitorAlignmentApp
from hwmonitor.ui.ui_util import load_icon


def main():
    qt_app = QApplication(sys.argv)
    qt_app.setWindowIcon(load_icon('icon.ico'))
    qt_app.setQuitOnLastWindowClosed(True)
    qt_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)

    app = HwMonitorAlignmentApp()
    app.start()

    exit_code = qt_app.exec_()
    app.finalize(exit_code)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
