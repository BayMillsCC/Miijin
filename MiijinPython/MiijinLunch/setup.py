from cx_Freeze import setup, Executable

setup(name="MiijinPy",
      version="0.1",
      description="Python program for collecting lunch IDs",
      executables=[Executable("MiijinLunch.py")])