from backend.monitor_backend import BaseMonitorBackend
from core.monitor import Monitor
from win32.flags import SystemMetricsFlags, MONITORINFO_FLAGS, QUERY_DEVICE_CONFIG_FLAGS, DISPLAYCONFIG_DEVICE_INFO_TYPE
from win32.func import GetSystemMetrics, GetMonitorInfoEx, EnumDisplaySettings, EnumDisplayDevices, EnumDisplayMonitors, \
    GetDisplayConfigBufferSizes, QueryDisplayConfig, DisplayConfigGetDeviceInfo
from win32.structs.displayconfig import DISPLAYCONFIG_SOURCE_DEVICE_NAME, DISPLAYCONFIG_TARGET_DEVICE_NAME


class Win32Backend(BaseMonitorBackend):

    def __init__(self):
        super().__init__()

        self._scan_monitors()

    def get_vscreen_size(self):
        width = GetSystemMetrics(SystemMetricsFlags.CXVIRTUALSCREEN)
        height = GetSystemMetrics(SystemMetricsFlags.CYVIRTUALSCREEN)
        return width, height

    def get_vscreen_normalize_offset(self):
        x = GetSystemMetrics(SystemMetricsFlags.XVIRTUALSCREEN)
        y = GetSystemMetrics(SystemMetricsFlags.YVIRTUALSCREEN)
        return x, y

    def get_monitor_order(self):
        return sorted(
            self.monitor_model.as_list(),
            key=lambda monitor: monitor.position_x
        )

    def _scan_monitors(self):
        path_count, mode_count = GetDisplayConfigBufferSizes(QUERY_DEVICE_CONFIG_FLAGS.ONLY_ACTIVE_PATHS)
        display_paths, display_modes = QueryDisplayConfig(QUERY_DEVICE_CONFIG_FLAGS.ONLY_ACTIVE_PATHS, path_count,
                                                          mode_count)

        def _proc_monitor(hmonitor, hdc, lprect, lparam):
            # Gather information
            monitor_info = GetMonitorInfoEx(hmonitor)
            devmode = EnumDisplaySettings(monitor_info.szDevice, 0)
            display_device = EnumDisplayDevices(monitor_info.szDevice, 0, 0)
            source_device_name = DISPLAYCONFIG_SOURCE_DEVICE_NAME()
            target_device_name = DISPLAYCONFIG_TARGET_DEVICE_NAME()

            for path in display_paths:
                DisplayConfigGetDeviceInfo(source_device_name, DISPLAYCONFIG_DEVICE_INFO_TYPE.GET_SOURCE_NAME,
                                           path.sourceInfo.adapterId, path.sourceInfo.id)
                if monitor_info.szDevice == source_device_name.viewGdiDeviceName:
                    target_device_name = DISPLAYCONFIG_TARGET_DEVICE_NAME()
                    DisplayConfigGetDeviceInfo(target_device_name, DISPLAYCONFIG_DEVICE_INFO_TYPE.GET_TARGET_NAME,
                                               path.sourceInfo.adapterId, path.targetInfo.id)

            # Create Monitor Item
            model_item = Monitor(device_name=monitor_info.szDevice,
                                 monitor_name=target_device_name.monitorFriendlyDeviceName,
                                 display_monitor=display_device.DeviceString,
                                 screen_width=monitor_info.rcMonitor.right - monitor_info.rcMonitor.left,
                                 screen_height=monitor_info.rcMonitor.bottom - monitor_info.rcMonitor.top,
                                 position_x=monitor_info.rcMonitor.left,
                                 position_y=monitor_info.rcMonitor.top,
                                 orientation=devmode.DUMMYUNIONNAME.DUMMYSTRUCTNAME2.dmDisplayOrientation,
                                 primary=MONITORINFO_FLAGS.PRIMARY in MONITORINFO_FLAGS(monitor_info.dwFlags))

            self.monitor_model.add(model_item)
            return True

        EnumDisplayMonitors(None, None, _proc_monitor, 0)
