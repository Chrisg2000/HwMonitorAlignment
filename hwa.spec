# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_submodules, get_package_paths

block_cipher = None

data = [
    ('hwmonitor/res/*', './hwmonitor/res')
]


# Preventing some kind if bug
hiddenimports = [
    'shibokensupport',
    'shibokensupport.signature.lib',
    'shibokensupport.signature.lib.enum_sig',
    'shibokensupport.signature.lib.tool',
    'shibokensupport.signature.layout',
    'shibokensupport.signature.loader',
    'shibokensupport.signature.parser',
    'shibokensupport.signature.mapping',
    'shibokensupport.signature.errorhandler',
]
hiddenimports += collect_submodules('lib.win32')


# adding shibokensupport to import path
pathex = [
    os.path.join(get_package_paths("shiboken2")[1], 'files.dir')
]

# minimize size
excludes = [
    'email',
    'pprint',
    'bdb',
    'pdb',
    'calendar',
    'doctest',
    'ftplib',
    'html',
    'http',
    'netrc',
    'pydoc',
    'ssl',
    'unittest',
    'urllib',
    'webbrowser',
    'xml',

    # Doing something scary
    'PySide2.QtPrintSupport',
    'PySide2.QtSql',
    'PySide2.QtNetwork',
    'PySide2.QtTest',
    'PySide2.QtConcurrent',
    'PySide2.QtXml',
    'PySide2.QtXmlPatterns',
    'PySide2.QtHelp',
    'PySide2.QtMultimedia',
    'PySide2.QtMultimediaWidgets',
    'PySide2.QtQml',
    'PySide2.QtQuick',
    'PySide2.QtQuickWidgets',
    'PySide2.QtRemoteObjects',
    'PySide2.QtScxml',
    'PySide2.QtScript',
    'PySide2.QtScriptTools',
    'PySide2.QtSensors',
    'PySide2.QtTextToSpeech',
    'PySide2.QtCharts',
    'PySide2.QtSvg',
    'PySide2.QtDataVisualization',
    'PySide2.QtAxContainer',
    'PySide2.QtWebChannel',
    'PySide2.QtWebEngineCore',
    'PySide2.QtWebEngine',
    'PySide2.QtWebEngineWidgets',
    'PySide2.QtWebSockets',
    'PySide2.Qt3DCore',
    'PySide2.Qt3DRender',
    'PySide2.Qt3DInput',
    'PySide2.Qt3DLogic',
    'PySide2.Qt3DAnimation',
    'PySide2.Qt3DExtras'
]


a = Analysis(['hwa.py'],
             pathex=pathex,
             binaries=[],
             datas=data,
             hiddenimports=hiddenimports,
             hookspath=[],
             runtime_hooks=[],
             excludes=excludes,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='HwMonitorAlignment',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False,
          uac_admin=False,
          icon='hwmonitor/res/icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name='HwMonitorAlignment')
