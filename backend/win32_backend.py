from backend.monitor_backend import BaseMonitorBackend
from core.monitor import Monitor
from win32.func import GetSystemMetrics, GetMonitorInfoEx, EnumDisplaySettings, EnumDisplayDevices, EnumDisplayMonitors
from win32.structs.monitorinfo import MONITORINFO_FLAGS
from win32.structs.system_metrics import SystemMetricsFlags


class Win32Backend(BaseMonitorBackend):

    def __init__(self):
        super().__init__()

        self._scan_monitors()

    def get_vscreen_size(self):
        width = GetSystemMetrics(SystemMetricsFlags.SM_CXVIRTUALSCREEN)
        height = GetSystemMetrics(SystemMetricsFlags.SM_CYVIRTUALSCREEN)
        return width, height

    def get_vscreen_normalize_offset(self):
        x = GetSystemMetrics(SystemMetricsFlags.SM_XVIRTUALSCREEN)
        y = GetSystemMetrics(SystemMetricsFlags.SM_YVIRTUALSCREEN)
        return x, y

    def _scan_monitors(self):
        def _proc_monitor(hmonitor, hdc, lprect, lparam):
            # Gather information
            monitor_info = GetMonitorInfoEx(hmonitor)
            devmode = EnumDisplaySettings(monitor_info.szDevice, 0)
            display_device = EnumDisplayDevices(monitor_info.szDevice, 0, 0)

            # Create Monitor Item
            model_item = Monitor(device_name=monitor_info.szDevice,
                                 monitor_name=display_device.DeviceString,
                                 screen_width=monitor_info.rcMonitor.right - monitor_info.rcMonitor.left,
                                 screen_height=monitor_info.rcMonitor.bottom - monitor_info.rcMonitor.top,
                                 position_x=monitor_info.rcMonitor.left,
                                 position_y=monitor_info.rcMonitor.top,
                                 orientation=devmode.DUMMYUNIONNAME.DUMMYSTRUCTNAME2.dmDisplayOrientation,
                                 primary=MONITORINFO_FLAGS.MONITORINFOF_PRIMARY in MONITORINFO_FLAGS(
                                     monitor_info.dwFlags))

            self.monitor_model.add(model_item)
            return True

        EnumDisplayMonitors(None, None, _proc_monitor, 0)
