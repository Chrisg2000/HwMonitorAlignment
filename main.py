import sys

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication

from app import HwMonitorAlignmentApp


def main():
    qt_app = QApplication(sys.argv)
    qt_app.setQuitOnLastWindowClosed(True)
    qt_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)

    app = HwMonitorAlignmentApp()
    app.start()

    exit_code = qt_app.exec_()
    app.finalize(exit_code)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
