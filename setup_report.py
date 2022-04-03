import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

directory_table = [
    ("ProgramMenuFolder", "TARGETDIR", "."),
    ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|Miijin Report"),
]

shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "Miijin Report",           # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]MiijinReport.exe",  # Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     ),
    ("StartMenuShortcut",        # Shortcut
     "ProgramMenuFolder",          # Directory_
     "Miijin Report",           # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]MiijinReport.exe",  # Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
    ]

msi_data = {
    "Directory": directory_table,
    "ProgId": [
        ("Prog.Id", None, None, "Miijin Report Program", "IconId", None),
    ],
    "Icon": [
        ("IconId", "icons/MiijinReportWindows.ico"),
    ],
    "Shortcut": shortcut_table
}

bdist_msi_options = {
    "add_to_path": True,
    "upgrade_code": '{C64E295A-C61B-30C9-9D17-A97ACD6C3218}',
    "data": msi_data
}

setup(
        name="Miijin Report",
        version="0.3",
        author='Bay Mills Community College',
        author_email='tpostma@bmcc.edu',
        url='https://github.com/BayMillsCC/Miijin',
        description="Pulls Data from SQL into Excel File",
        executables=[Executable("src/Miijin/MiijinReport/MiijinReport.py", base=base,
                                icon="icons/MiijinReportWindows.ico"
                                )],
        options={'bdist_mac': {'iconfile': 'icons/MiijinReport.icns'},
                 'bdist_msi': bdist_msi_options}
)
