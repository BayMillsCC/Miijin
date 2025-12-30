import sys
from cx_Freeze import setup, Executable

base = "Win32GUI" if sys.platform == "win32" else None
exe_icon = "icons/MiijinLunchWindows.ico" if sys.platform == "win32" else None

executables = [
    Executable(
        "src/Miijin/MiijinLunch/MiijinLunch.py",
        base=base,
        icon=exe_icon,
        target_name="MiijinLunch.exe" if sys.platform == "win32" else "MiijinLunch",
    )
]

options = {
    # Always useful: bundle non-Python runtime assets your GUI needs.
    "build_exe": {
        "include_files": [
            ("icons", "icons"),
        ],
    },

    # macOS builder
    "bdist_mac": {
        "iconfile": "icons/MiijinLunch.icns",
    },

    # Debian (.deb) builder for Raspberry Pi OS / Debian (arm64).
    "bdist_deb": {
        # --- Tkinter ---
        "depends": ["python3-tk"],
        "maintainer": "Bay Mills Community College <tpostma@bmcc.edu>",
    },
}

if sys.platform == "win32":
    directory_table = [
        ("ProgramMenuFolder", "TARGETDIR", "."),
        ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|Miijin Lunch"),
    ]

    shortcut_table = [
        (
            "DesktopShortcut",          # Shortcut
            "DesktopFolder",            # Directory_
            "Miijin Lunch",             # Name
            "TARGETDIR",                # Component_
            "[TARGETDIR]MiijinLunch.exe",  # Target
            None,                       # Arguments
            None,                       # Description
            None,                       # Hotkey
            None,                       # Icon
            None,                       # IconIndex
            None,                       # ShowCmd
            "TARGETDIR",                # WkDir
        ),
        (
            "StartMenuShortcut",        # Shortcut
            "ProgramMenuFolder",        # Directory_
            "Miijin Lunch",             # Name
            "TARGETDIR",                # Component_
            "[TARGETDIR]MiijinLunch.exe",  # Target
            None,                       # Arguments
            None,                       # Description
            None,                       # Hotkey
            None,                       # Icon
            None,                       # IconIndex
            None,                       # ShowCmd
            "TARGETDIR",                # WkDir
        ),
    ]

    msi_data = {
        "Directory": directory_table,
        "ProgId": [
            ("Prog.Id", None, None, "Miijin Lunch Program", "IconId", None),
        ],
        "Icon": [
            ("IconId", "icons/MiijinLunchWindows.ico"),
        ],
        "Shortcut": shortcut_table,
    }

    bdist_msi_options = {
        "add_to_path": True,
        "upgrade_code": "{9724B7AA-9800-33A2-8DF4-A1164248B8EE}",
        "data": msi_data,
    }

    options["bdist_msi"] = bdist_msi_options

# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------
setup(
    name="Miijin Lunch",
    version="1.1",
    author="Bay Mills Community College",
    author_email="tpostma@bmcc.edu",
    url="https://github.com/BayMillsCC/Miijin",
    description="Scans IDs into SQL database",
    executables=executables,
    options=options,
)
