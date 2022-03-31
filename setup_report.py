import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
        name="Miijin Report",
        version="0.1",
        description="Pulls Data from SQL into Excel File",
        icon='icons/MiijinReportWindows.ico',
        executables=[Executable("src/Miijin/MiijinReport/MiijinReport.py", base=base)],
        options={'bdist_mac': {'iconfile': 'icons/MiijinReport.icns'}}
)
