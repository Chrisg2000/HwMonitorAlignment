from copy import deepcopy

from hwmonitor.monitors.monitor import Monitor, MonitorOrientation


class MonitorFactory:

    @classmethod
    def create_monitor(cls, device_name, **kwargs):
        """Return a new monitor item

        :param device_name: necessary device name
        :keyword monitor_name: OS related name of the associated display device
        :keyword friendly_monitor_name: Easy-to-understand name of the monitor
        :keyword display_adapter: Display Adapter of the display device

        :keyword screen_width: Width of the screen in pixels
        :keyword screen_height: Height of the screen in pixels
        :keyword position_x: x-position of the screen on the virtual screen in pixel-coordinates
        :keyword position_y: y-position of the screen on the virtual screen in pixel-coordinates
        :keyword orientation: Real-world orientation of the display device
        :keyword primary: Whether the display device is the primary one or not
        """
        monitor = Monitor()

        monitor.device_name = device_name
        monitor.monitor_name = kwargs.pop('monitor_name', '')
        monitor.friendly_monitor_name = kwargs.pop('friendly_monitor_name', '')
        monitor.display_adapter = kwargs.pop('display_adapter', '')

        monitor.screen_width = kwargs.pop('screen_width', 0)
        monitor.screen_height = kwargs.pop('screen_height', 0)
        monitor.position_x = kwargs.pop('position_x', 0)
        monitor.position_y = kwargs.pop('position_y', 0)
        monitor.orientation = kwargs.pop('orientation', MonitorOrientation.Landscape)

        monitor.primary = kwargs.pop('primary', False)

        return monitor

    @classmethod
    def clone_monitor(cls, monitor):
        """Return a copy of existing monitor item"""
        properties = deepcopy(monitor.properties())

        monitor = cls.create_monitor(**properties)

        return monitor
