import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

directory_table = [
    ("ProgramMenuFolder", "TARGETDIR", "."),
    ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|Miijin Lunch"),
]

shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "Miijin Lunch",           # Name
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
     "Miijin Lunch",           # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]MiijinLunch.exe",  # Target
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
        ("Prog.Id", None, None, "Miijin Lunch Program", "IconId", None),
    ],
    "Icon": [
        ("IconId", "icons/MiijinLunchWindows.ico"),
    ],
    "Shortcut": shortcut_table
}

bdist_msi_options = {
    "add_to_path": True,
    "data": msi_data
}

setup(
        name="Miijin Lunch",
        version="0.1",
        author='Tyler Postma',
        author_email='tpostma@bmcc.edu',
        url='https://github.com/BayMillsCC/Miijin',
        description="Scans IDs into SQL database",
        executables=[Executable("src/Miijin/MiijinLunch/MiijinLunch.py", base=base,
                                icon="icons/MiijinLunchWindows.ico"
                                )],
        options={'bdist_mac': {'iconfile': 'icons/MiijinLunch.icns'},
                 'bdist_msi': bdist_msi_options}
)
