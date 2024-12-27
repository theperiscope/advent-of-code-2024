# Development Notes

1. [How to complile Python script to .exe](#how-to-complile-python-script-to-exe)
   1. [Install PyInstaller](#install-pyinstaller)
   1. [Compile your script](#compile-your-script)
   1. [Find your executable](#find-your-executable)
   1. [Performance timing with a custom decorator](#performance-timing-with-a-custom-decorator)


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

### Performance timing with a custom decorator

```python
from typing import Any
from time import perf_counter_ns


def profiler(method):
    def wrapper_method(*args: Any, **kwargs: Any) -> Any: # interesting: keywords args in a wrapper
        start_time = perf_counter_ns()
        ret = method(*args, **kwargs)
        stop_time = perf_counter_ns() - start_time
        time_len = min(9, ((len(str(stop_time)) - 1) // 3) * 3)
        time_conversion = {9: "seconds", 6: "milliseconds", 3: "microseconds", 0: "nanoseconds"}
        print(f"Method {method.__name__} took : {
              stop_time / (10**time_len)} {time_conversion[time_len]}")
        return ret

    return wrapper_method


@profiler  # interesting: custom Python decorators - takes a function, extends it and returns a function
def sample_usage():
    pass

```
