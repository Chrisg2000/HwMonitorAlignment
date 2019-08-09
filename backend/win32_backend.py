from _ctypes import byref

from backend.backend import Backend
from core.list_model import ListModel
from core.monitor_model import MonitorModel
from win32.func import GetMonitorInfoExW, MonitorEnumProc, EnumDisplayMonitors, EnumDisplayDevicesW, GetSystemMetrics, \
    EnumDisplaySettingsW
from win32.structs.devmode import DEVMODE
from win32.structs.display_device import DISPLAY_DEVICE
from win32.structs.monitorinfo import MONITORINFOEX, MONITORINFO_FLAGS
from win32.structs.system_metrics import SystemMetricsFlags


class Win32Backend(Backend):

    def __init__(self):
        super().__init__()

    def get_monitor_model(self, refresh=False) -> ListModel:
        if self._monitor_model.empty() or refresh:
            if refresh:
                self._monitor_model.reset()
            self._scan_monitors()
        return self._monitor_model

    def get_vscreen_size(self):
        width = GetSystemMetrics(SystemMetricsFlags.SM_CXVIRTUALSCREEN)
        height = GetSystemMetrics(SystemMetricsFlags.SM_CYVIRTUALSCREEN)
        return width, height

    def get_vscreen_normalize_offset(self):
        x = GetSystemMetrics(SystemMetricsFlags.SM_XVIRTUALSCREEN)
        y = GetSystemMetrics(SystemMetricsFlags.SM_YVIRTUALSCREEN)
        return x, y

    def _scan_monitors(self):
        @MonitorEnumProc
        def _proc_monitor(hmonitor, hdc, lprect, lparam):
            model_item = MonitorModel()

            monitor_info = MONITORINFOEX()
            GetMonitorInfoExW(hmonitor, byref(monitor_info))

            display_device = DISPLAY_DEVICE()
            EnumDisplayDevicesW(monitor_info.szDevice, 0, byref(display_device), 0)

            devmode = DEVMODE()
            EnumDisplaySettingsW(monitor_info.szDevice, 0, byref(devmode))

            model_item.device_name = monitor_info.szDevice
            model_item.monitor_name = display_device.DeviceString
            model_item.primary = MONITORINFO_FLAGS.MONITORINFOF_PRIMARY in MONITORINFO_FLAGS(monitor_info.dwFlags)

            model_item.screen_width = monitor_info.rcMonitor.right - monitor_info.rcMonitor.left
            model_item.screen_height = monitor_info.rcMonitor.bottom - monitor_info.rcMonitor.top
            model_item.position_x = monitor_info.rcMonitor.left
            model_item.position_y = monitor_info.rcMonitor.top
            model_item.orientation = devmode.DUMMYUNIONNAME.DUMMYSTRUCTNAME2.dmDisplayOrientation

            self._monitor_model.add(model_item)
            return True

        EnumDisplayMonitors(None, None, _proc_monitor, 0)
