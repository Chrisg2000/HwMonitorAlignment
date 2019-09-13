# Custom Windows-User32 API

This is a custom ctypes implementation of some Windows user32 used in the
parent project. The API will be extended in the future, depending on 
what functions are needed.

## Mapped Functions
### [ChangeDisplaySettingsEx](https://docs.microsoft.com/windows/win32/api/winuser/nf-winuser-changedisplaysettingsexw):
The ChangeDisplaySettingsEx function changes the settings of the specified display
device to the specified graphics mode. 
```c
LONG ChangeDisplaySettingsExW(
  LPCWSTR  lpszDeviceName,
  DEVMODEW *lpDevMode,
  HWND     hwnd,
  DWORD    dwflags,
  LPVOID   lParam
);
```
Python implementation:
```python
def ChangeDisplaySettingsEx(lpszDeviceName, lpDevMode, dwflags, lParam=None): ...
```

Returned Devmode structure:
```c
typedef struct _devicemodeW {
  WCHAR dmDeviceName[CCHDEVICENAME];
  WORD  dmSpecVersion;
  WORD  dmDriverVersion;
  WORD  dmSize;
  WORD  dmDriverExtra;
  DWORD dmFields;
  union {
    struct {
      short dmOrientation;
      short dmPaperSize;
      short dmPaperLength;
      short dmPaperWidth;
      short dmScale;
      short dmCopies;
      short dmDefaultSource;
      short dmPrintQuality;
    } DUMMYSTRUCTNAME;
    POINTL dmPosition;
    struct {
      POINTL dmPosition;
      DWORD  dmDisplayOrientation;
      DWORD  dmDisplayFixedOutput;
    } DUMMYSTRUCTNAME2;
  } DUMMYUNIONNAME;
  short dmColor;
  short dmDuplex;
  short dmYResolution;
  short dmTTOption;
  short dmCollate;
  WCHAR dmFormName[CCHFORMNAME];
  WORD  dmLogPixels;
  DWORD dmBitsPerPel;
  DWORD dmPelsWidth;
  DWORD dmPelsHeight;
  union {
    DWORD dmDisplayFlags;
    DWORD dmNup;
  } DUMMYUNIONNAME2;
  DWORD dmDisplayFrequency;
  DWORD dmICMMethod;
  DWORD dmICMIntent;
  DWORD dmMediaType;
  DWORD dmDitherType;
  DWORD dmReserved1;
  DWORD dmReserved2;
  DWORD dmPanningWidth;
  DWORD dmPanningHeight;
} DEVMODEW, *PDEVMODEW, *NPDEVMODEW, *LPDEVMODEW;
```

### [GetDisplayConfigBufferSizes](https://docs.microsoft.com/windows/win32/api/winuser/nf-winuser-getdisplayconfigbuffersizes):
The GetDisplayConfigBufferSizes function retrieves the size of the buffers that are required
to call the QueryDisplayConfig function.
```c
LONG GetDisplayConfigBufferSizes(
  UINT32 flags,
  UINT32 *numPathArrayElements,
  UINT32 *numModeInfoArrayElements
);
```
Python implementation:
```python
def GetDisplayConfigBufferSizes(flags): ...
```

### [QueryDisplayConfig](https://docs.microsoft.com/windows/desktop/api/winuser/nf-winuser-querydisplayconfig):
The QueryDisplayConfig function retrieves information about all possible display paths for all display devices,
or views, in the current setting.
```c
LONG QueryDisplayConfig(
  UINT32                    flags,
  UINT32                    *numPathArrayElements,
  DISPLAYCONFIG_PATH_INFO   *pathArray,
  UINT32                    *numModeInfoArrayElements,
  DISPLAYCONFIG_MODE_INFO   *modeInfoArray,
  DISPLAYCONFIG_TOPOLOGY_ID *currentTopologyId
);
```
Python implementation:
```python
def QueryDisplayConfig(flags, numPathArrayElements, numModeInfoArrayElements): ...
```

### [DisplayConfigGetDeviceInfo](https://docs.microsoft.com/windows/win32/api/winuser/nf-winuser-displayconfiggetdeviceinfo):
The DisplayConfigGetDeviceInfo function retrieves display configuration information about the device.
```c
LONG DisplayConfigGetDeviceInfo(
  DISPLAYCONFIG_DEVICE_INFO_HEADER *requestPacket
);
```
Python implementation:
```python
def DisplayConfigGetDeviceInfo(target: Any, type_, adapterId, id_): ...
```

### [EnumDisplayDevices](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumdisplaydevicesw):
The EnumDisplayDevices function lets you obtain information about the display devices in the current session.
```c
BOOL EnumDisplayDevicesW(
  LPCWSTR          lpDevice,
  DWORD            iDevNum,
  PDISPLAY_DEVICEW lpDisplayDevice,
  DWORD            dwFlags
);
```
Python implementation:
```python
def EnumDisplayDevices(lpDevice, iDevNum, dwFlags): ...
```

Returned DisplayDevice structure:
```c
typedef struct _DISPLAY_DEVICEW {
  DWORD cb;
  WCHAR DeviceName[32];
  WCHAR DeviceString[128];
  DWORD StateFlags;
  WCHAR DeviceID[128];
  WCHAR DeviceKey[128];
} DISPLAY_DEVICEW, *PDISPLAY_DEVICEW, *LPDISPLAY_DEVICEW;
```

### [EnumDisplaySettings](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumdisplaysettingsw):
The EnumDisplaySettings function retrieves information about one of the graphics modes for a display device.
To retrieve information for all the graphics modes of a display device, make a series of calls to this function.
```c
BOOL EnumDisplaySettingsW(
  LPCWSTR  lpszDeviceName,
  DWORD    iModeNum,
  DEVMODEW *lpDevMode
);
```
Python implementation:
```python
def EnumDisplaySettings(lpszDeviceName, iModeNum): ...
```

### [EnumDisplayMonitors](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumdisplaymonitors):
The EnumDisplayMonitors function enumerates display monitors (including invisible pseudo-monitors associated with
the mirroring drivers) that intersect a region formed by the intersection of a specified clipping rectangle and
the visible region of a device context. EnumDisplayMonitors calls an application-defined MonitorEnumProc callback
function once for each monitor that is enumerated. Note that GetSystemMetrics (SM_CMONITORS)
counts only the display monitors.
```c
BOOL EnumDisplaySettingsW(
  LPCWSTR  lpszDeviceName,
  DWORD    iModeNum,
  DEVMODEW *lpDevMode
);
```
Python implementation:
```python
def EnumDisplayMonitors(hdc, lpreClip, lpfnEnum, dwData): ...
```

### [GetMonitorInfo](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getmonitorinfow):
The GetMonitorInfo function retrieves information about a display monitor.
```c
BOOL GetMonitorInfoW(
  HMONITOR      hMonitor,
  LPMONITORINFO lpmi
);
```
Python implementation:
```python
def GetMonitorInfo(hMonitor): ...
```

Returned MonitorInfo strucuture:
```c
typedef struct tagMONITORINFO {
DWORD cbSize;
  RECT  rcMonitor;
  RECT  rcWork;
  DWORD dwFlags;
} MONITORINFO, *LPMONITORINFO;
```

### [GetMonitorInfoEx](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getmonitorinfow):
The GetMonitorInfo function retrieves information about a display monitor.
```c
BOOL GetMonitorInfoW(
  HMONITOR      hMonitor,
  LPMONITORINFO lpmi
);
```
Python implementation:
```python
def GetMonitorInfoEx(hMonitor): ...
```

Returned MonitorInfoEx strucuture:
```c
typedef struct tagMONITORINFOEX {
  DWORD cbSize;
  RECT  rcMonitor;
  RECT  rcWork;
  DWORD dwFlags;
  TCHAR szDevice[CCHDEVICENAME];
} MONITORINFOEX, *LPMONITORINFOEX;
```

### [GetSystemMetrics](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsystemmetrics):
Retrieves the specified system metric or system configuration setting.
Note that all dimensions retrieved by GetSystemMetrics are in pixels.
```c
int GetSystemMetrics(
  int nIndex
);
```
Python implementation:
```python
def GetSystemMetrics(nIndex): ...
```

