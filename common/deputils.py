import importlib
import importlib.util
import sys

PLEASE_INSTALL_MODULES = "Please install dependency modules by doing this(use pip or pip3):\n"

already_imported = {}


def check_import(dependency):
    """
    Checks for the existence and availability of the dependency module

    :param dependency: the name of the dependency module to check for
    :return: True if the module is available, False otherwise
    """
    result = False
    spec_not_found = (spec := importlib.util.find_spec(dependency)) is None

    if spec_not_found:
        print(PLEASE_INSTALL_MODULES)
        print(f"> pip install {dependency!r}")
    else:
        result = True

    print(f'Checking dependency {dependency}: {result}')
    return result


def do_import(dependency):
    """
    Imports the dependency module

    :param dependency: the name of the dependency module to import
    :raise: ModuleNotFoundError if not found
    :return: the imported module
    """
    global already_imported
    if dependency in already_imported:
        result_module = already_imported[dependency]
    else:
        result_module = importlib.import_module(dependency)
        already_imported[dependency] = result_module

    return result_module
