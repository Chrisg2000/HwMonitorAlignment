from hwmonitor.backend.backend import Backend
from hwmonitor.module.win32_backend.win32_monitor import Win32Monitor
from hwmonitor.module.win32_backend.win32_vscreen import Win32VScreen
from hwmonitor.monitors.monitor_model import MonitorModel
from hwmonitor.vscreen.vscreen import VScreen
from lib.win32.flags import ChangeDisplaySettings, DevmodeSettings, DevmodeFieldFlags, DisplayDeviceFlags, \
    QueryDeviceConfigFlags, DisplayConfigDeviceInfoType, SystemMetricsFlags
from lib.win32.func import GetSystemMetrics, ChangeDisplaySettingsEx, EnumDisplaySettings, GetDisplayConfigBufferSizes, \
    QueryDisplayConfig, DisplayConfigGetDeviceInfo, EnumDisplayDevices
from lib.win32.structs import DISPLAYCONFIG_TARGET_DEVICE_NAME


# noinspection PyMethodMayBeStatic
class Win32Backend(Backend):

    def get_vscreen(self) -> VScreen:
        model = MonitorModel()
        self._discover_monitors(model)
        return Win32VScreen(model, self)

    def get_vscreen_size(self):
        width = GetSystemMetrics(SystemMetricsFlags.CXVIRTUALSCREEN)
        height = GetSystemMetrics(SystemMetricsFlags.CYVIRTUALSCREEN)
        return width, height

    def get_vscreen_offset(self):
        x = GetSystemMetrics(SystemMetricsFlags.XVIRTUALSCREEN)
        y = GetSystemMetrics(SystemMetricsFlags.YVIRTUALSCREEN)
        return x, y

    def set_monitor_position(self, device_name, x: int, y: int, *, reset=True):
        if device_name is None:
            # Apply settings
            return ChangeDisplaySettingsEx(None, None, 0, None)
        devmode = EnumDisplaySettings(device_name,
                                      DevmodeSettings.ENUM_REGISTRY_SETTINGS)
        devmode.dmPosition = (x, y)
        devmode.dmFields = DevmodeFieldFlags.POSITION  # only change the position of the screen

        update_flags = ChangeDisplaySettings.UPDATEREGISTRY | ChangeDisplaySettings.GLOBAL
        if not reset:
            return ChangeDisplaySettingsEx(device_name,
                                           devmode,
                                           update_flags |
                                           ChangeDisplaySettings.NORESET,
                                           None)

        return ChangeDisplaySettingsEx(device_name,
                                       devmode,
                                       update_flags,
                                       None)

    def _discover_friendly_names(self):
        path_count, mode_count = GetDisplayConfigBufferSizes(QueryDeviceConfigFlags.ONLY_ACTIVE_PATHS)
        display_paths, display_modes = QueryDisplayConfig(QueryDeviceConfigFlags.ONLY_ACTIVE_PATHS, path_count,
                                                          mode_count)
        monitor_friendly_device_names = {}
        for path in display_paths:
            target_device_name = DISPLAYCONFIG_TARGET_DEVICE_NAME()
            DisplayConfigGetDeviceInfo(target_device_name, DisplayConfigDeviceInfoType.GET_TARGET_NAME,
                                       path.sourceInfo.adapterId, path.targetInfo.id)
            monitor_friendly_device_names[
                target_device_name.monitorDevicePath] = target_device_name.monitorFriendlyDeviceName
        return monitor_friendly_device_names

    def _discover_monitors(self, model):
        monitor_friendly_device_names = self._discover_friendly_names()

        i_dev_num = 0
        while i_dev_num < 1000:  # prevent infinite loop
            try:
                display_device = EnumDisplayDevices(None, i_dev_num, 0)
                dev_mon = 0
                while dev_mon < 1000:  # prevent inner infinite loop
                    try:
                        display_device_monitor = EnumDisplayDevices(display_device.DeviceName, dev_mon, 1)

                        if display_device_monitor.StateFlags & DisplayDeviceFlags.ATTACHED_TO_DESKTOP and \
                                not display_device_monitor.StateFlags & DisplayDeviceFlags.MIRRORING_DRIVER:
                            devmode = EnumDisplaySettings(display_device.DeviceName,
                                                          DevmodeSettings.ENUM_REGISTRY_SETTINGS)

                            item = Win32Monitor(
                                device_name=display_device.DeviceName,
                                monitor_name=display_device_monitor.DeviceString,
                                friendly_monitor_name=monitor_friendly_device_names[display_device_monitor.DeviceID],
                                display_adapter=display_device.DeviceString,
                                screen_width=devmode.dmPelsWidth,
                                screen_height=devmode.dmPelsHeight,
                                position_x=devmode.DUMMYUNIONNAME.dmPosition.x,
                                position_y=devmode.DUMMYUNIONNAME.dmPosition.y,
                                orientation=devmode.DUMMYUNIONNAME.DUMMYSTRUCTNAME2.dmDisplayOrientation,
                                primary=bool(display_device.StateFlags & DisplayDeviceFlags.PRIMARY_DEVICE))
                            item.set_backend(self)

                            model.add(item)
                        dev_mon += 1
                    except WindowsError:
                        break
                i_dev_num += 1
            except WindowsError:
                break
