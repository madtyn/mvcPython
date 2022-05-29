import sys

from common.constants import MISSING_DEPENDENCIES_ERROR_CODE
from common.deputils import check_import, do_import
from controller.controller import Controller
from model.model import Model

PLEASE_INSTALL_MODULES = "Please install dependency modules by doing this(use pip or pip3):\n"

dependencies = ['tkfilebrowser', 'tkcalendar']

warning = not all([check_import(dep) for dep in dependencies])

if warning:
    sys.exit(MISSING_DEPENDENCIES_ERROR_CODE)

from view.view import GuiView

try:
    for i in range(len(dependencies)):
        d = dependencies[i]
        do_import(d)
except ModuleNotFoundError as e:
    print(PLEASE_INSTALL_MODULES)
    if e.name == 'win32com':
        print(f"C:\> pip install pywin32")
        print(f"$ pip install pywin32")
    else:
        print(f"C:\> pip install {d}")
        print(f"$ pip install {d}")
    sys.exit(0)

if __name__ == '__main__':
    model = Model()
    if 'text' in sys.argv:
        controller = Controller(model, TerminalView)
    else:
        controller = Controller(model, GuiView)
    controller.start()
