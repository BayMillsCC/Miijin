import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
        name="Miijin Lunch",
        version="0.1",
        description="Scans IDs into SQL database",
        icon='icons/MiijinLunchWindows.ico',
        executables=[Executable("src/Miijin/MiijinLunch/MiijinLunch.py", base=base)],
        options={'bdist_mac': {'iconfile': 'icons/MiijinLunch.icns'}}
)
