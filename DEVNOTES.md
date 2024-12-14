# Development Notes

1. [How to complile Python script to .exe](#how-to-complile-python-script-to-exe)
   1. [Install PyInstaller](#install-pyinstaller)
   1. [Compile your script](#compile-your-script)
   1. [Find your executable](#find-your-executable)


## How to complile Python script to .exe

To compile a Python script to a .exe file on Windows x64, you can use a tool called `PyInstaller`.

### Install PyInstaller

Open your command prompt and run:

```batch
pip install pyinstaller
```

### Compile your script

Run PyInstaller with your script:

```batch
pyinstaller --onefile day01.py
```

The `--onefile` flag packages everything into a single executable.

### Find your executable

After the process completes, you the `.exe` file will be in the `dist\` directory at `dist\day01.exe`.
