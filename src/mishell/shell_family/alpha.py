import inspect
import mishell
import pkgutil

from os.path import isabs


class Alpha:
    def __init__(self):
        pass

    def __init_subclass__(cls, **kwargs):
        name = getattr(cls, "NAME", cls.__name__.lower())
        file_and_name = inspect.getfile(cls) + "::" + name
        ShellFamily.loaded_family[file_and_name] = cls

    def do(self, data, *args, **kwargs):
        raise NotImplementedError()

    def get_process_result(self):
        raise NotImplementedError()


family_loaded = set()


def load():
    global family_loaded

    paths = mishell.shell_family.__path__
    paths = {p for p in paths if isabs(p) and p not in family_loaded}
    if len(paths) == 0:
        print(f"paths is empty.")
        return

    modules_to_load = []
    for finder, name, _ in pkgutil.iter_modules(paths):
        found_module = finder.find_module(name)
        modules_to_load.append((name, found_module))

    for (name, module) in sorted(modules_to_load, key=lambda x: x[0]):
        try:
            _ = module.load_module(name)
        except Exception as e:
            print(f"Could not load family at '{name}':{e}")

    family_loaded.update(paths)


class ShellFamily:
    loaded_family = {}

    def __init__(self):
        self.registered_family = {}
        load()

    def initialize(self):
        for item in self.loaded_family.values():
            self.register_family(item)

    def register_family(self, family_class):
        name = getattr(family_class, "NAME", family_class.__name__.lower())
        family = family_class()
        self.registered_family[name] = family
        print(f"Successfully registered plugin '{name}'")

    def get_all_family(self):
        return [cls for cls in self.registered_family.values()]

    def get(self, family_name):
        return self.registered_family.get(family_name, None)

    def get_all_family_name(self):
        return [name for name in self.registered_family.keys()]
