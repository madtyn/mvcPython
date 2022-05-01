import sys
from pathlib import Path


from common import deputils
from common.observer import Observable
PLEASE_INSTALL_MODULES = "Please install dependency modules by doing this(use pip or pip3):\n"

dependency = 'tkfilebrowser'

deputils.check_import(dependency)

try:
    tkfilebrowser = deputils.do_import(dependency)
except ModuleNotFoundError as e:
    if e.name == 'win32com':
        print(PLEASE_INSTALL_MODULES)
        print(f"C:\> pip install pywin32")
        print(f"$ pip install pywin32")
        sys.exit(0)


class Model(Observable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == '__main__':
    m = Model()
    test_path = Path.home().resolve()
    m.collect_metrics(str(test_path), [str(Path('.').resolve())], 'test.json')
