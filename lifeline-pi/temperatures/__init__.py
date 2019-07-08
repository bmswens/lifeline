import os
import importlib

FUNCTIONS = {}


def get_temperatures(operating_system, **kwargs):
    if operating_system in FUNCTIONS:
        return FUNCTIONS[operating_system](**kwargs)
    else:
        raise NotImplementedError("{operating_system} is not currently supported.".format(
            operating_system=operating_system))


if __name__ != '__main__':
    folder = os.path.split(__file__)[0]
    for file in os.listdir(folder):
        if '.py' in file and file != '__init__.py':
            module_name = file.replace('.py', '')
            module = importlib.import_module("temperatures.{module_name}".format(module_name=module_name))
            FUNCTIONS[module_name] = module.main
