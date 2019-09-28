from PySide2.QtGui import QPixmap, QIcon

from hwmonitor.monitors.monitor import MonitorOrientation


def index_from_device_name(device_name: str) -> str:
    """Convert MS Windows device_name to an index.

    If device_name does not fit the pattern an empty string is returned
    """
    device_name_pattern = r"\\.\DISPLAY"
    if device_name.startswith(device_name_pattern):
        return device_name[len(device_name_pattern):]
    return ''


def label_orientation(orientation: MonitorOrientation):
    """Labels the MonitorOrientation enum"""
    if orientation == MonitorOrientation.Landscape:
        return 'Landscape'
    elif orientation == MonitorOrientation.Portrait:
        return 'Portrait'
    elif orientation == MonitorOrientation.FlippedLandscape:
        return 'Landscape (flipped)'
    elif orientation == MonitorOrientation.FlippedPortrait:
        return 'Portrait (flipped)'
    else:
        raise ValueError("orientation needs to be a DisplayOrientation")


def load_icon(icon_name):
    """Return a QIcon from the icon repository.

    The loaded icons are cached

    .. warning:
        QIcons should be loaded only from the QT main loop.
    """
    return QIcon('hwmonitor/res/' + icon_name)


def load_pixmap(pixmap_name):
    """Return a QPixmap from icon repository.

    The loaded pixmaps are cached

    ..warning:
        QPixmap should be loaded only from the QT main loop.
    :type pixmap_name: name of pixmap in icon folder
    :rtype: QPixmap
    """
    return QPixmap('hwmonitor/res/' + pixmap_name)
