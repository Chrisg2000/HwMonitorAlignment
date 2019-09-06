from backend.monitor_backend import BaseMonitorBackend
from monitors.monitor import Monitor
from win32.flags import SystemMetricsFlags, QUERY_DEVICE_CONFIG_FLAGS, \
    DISPLAYCONFIG_DEVICE_INFO_TYPE, DISPLAY_DEVICE_FLAGS, DEVICE_MODE_MODE
from win32.func import GetSystemMetrics, EnumDisplaySettings, EnumDisplayDevices, GetDisplayConfigBufferSizes, \
    QueryDisplayConfig, DisplayConfigGetDeviceInfo
from win32.structs.displayconfig import DISPLAYCONFIG_TARGET_DEVICE_NAME


class Win32Backend(BaseMonitorBackend):

    def __init__(self):
        super().__init__()

        self._discover_monitors()

    def get_vscreen_size(self):
        width = GetSystemMetrics(SystemMetricsFlags.CXVIRTUALSCREEN)
        height = GetSystemMetrics(SystemMetricsFlags.CYVIRTUALSCREEN)
        return width, height

    def get_vscreen_normalize_offset(self):
        x = GetSystemMetrics(SystemMetricsFlags.XVIRTUALSCREEN)
        y = GetSystemMetrics(SystemMetricsFlags.YVIRTUALSCREEN)
        return x, y

    def set_monitor_position(self, device_name: str, x: int, y: int):
        pass

    def _discover_monitors(self):
        path_count, mode_count = GetDisplayConfigBufferSizes(QUERY_DEVICE_CONFIG_FLAGS.ONLY_ACTIVE_PATHS)
        display_paths, display_modes = QueryDisplayConfig(QUERY_DEVICE_CONFIG_FLAGS.ONLY_ACTIVE_PATHS, path_count,
                                                          mode_count)

        monitor_friendly_device_names = {}
        for path in display_paths:
            target_device_name = DISPLAYCONFIG_TARGET_DEVICE_NAME()
            DisplayConfigGetDeviceInfo(target_device_name, DISPLAYCONFIG_DEVICE_INFO_TYPE.GET_TARGET_NAME,
                                       path.sourceInfo.adapterId, path.targetInfo.id)
            monitor_friendly_device_names[
                target_device_name.monitorDevicePath] = target_device_name.monitorFriendlyDeviceName

        i_dev_num = 0
        while i_dev_num < 1000:  # prevent infinite loop
            try:
                display_device = EnumDisplayDevices(None, i_dev_num, 0)
                dev_mon = 0
                while dev_mon < 1000:  # prevent inner infinite loop
                    try:
                        display_device_monitor = EnumDisplayDevices(display_device.DeviceName, dev_mon, 1)

                        if display_device_monitor.StateFlags & DISPLAY_DEVICE_FLAGS.ATTACHED_TO_DESKTOP and \
                                not display_device_monitor.StateFlags & DISPLAY_DEVICE_FLAGS.MIRRORING_DRIVER:
                            devmode = EnumDisplaySettings(display_device.DeviceName,
                                                          DEVICE_MODE_MODE.ENUM_REGISTRY_SETTINGS)

                            item = Monitor(
                                device_name=display_device.DeviceName,
                                monitor_name=display_device_monitor.DeviceString,
                                friendly_monitor_name=monitor_friendly_device_names[display_device_monitor.DeviceID],
                                display_adapter=display_device.DeviceString,
                                screen_width=devmode.dmPelsWidth,
                                screen_height=devmode.dmPelsHeight,
                                position_x=devmode.DUMMYUNIONNAME.dmPosition.x,
                                position_y=devmode.DUMMYUNIONNAME.dmPosition.y,
                                orientation=devmode.DUMMYUNIONNAME.DUMMYSTRUCTNAME2.dmDisplayOrientation,
                                primary=bool(display_device.StateFlags & DISPLAY_DEVICE_FLAGS.PRIMARY_DEVICE))

                            self.monitor_model.add(item)
                        dev_mon += 1
                    except WindowsError:
                        break
                i_dev_num += 1
            except WindowsError:
                break
