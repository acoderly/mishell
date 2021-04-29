import yara
import os
from typing import Dict

from mishell.shell_family import ShellFamily

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mishell/data")
YARA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mishell/shell_yara")
YARA_RULES = os.path.join(YARA_DIR, "include.yara")


def process_yara_include():
    lines = []
    for name in os.listdir(YARA_DIR):
        if name == "include.yara":
            continue
        lines.append(f"include \"./{name}\"\n")
    with open(YARA_RULES, "w+") as f:
        for line in lines:
            f.write(line)


def wrap_callback(file_abs_path, g_map):
    def callback(data):
        if data is None:
            return yara.CALLBACK_CONTINUE
        rule_name = data["rule"]
        family_dict = g_map.get(rule_name, {})
        anchor_dct = family_dict.get(file_abs_path, {})
        strings = data["strings"]
        for item in strings:
            _, name, value = item
            if name.startswith("$anchor"):
                value = value.decode("utf-8")
                name = name[1:]  # strip $
                if name not in anchor_dct.keys():
                    anchor_dct[name] = value

        family_dict[file_abs_path] = anchor_dct
        g_map[rule_name] = family_dict

        return yara.CALLBACK_CONTINUE

    return callback


current_ability = ["watchdogminer", "watchdogminer_scanner", "sysrv_sh"]
family_dispatch_map = {}

process_yara_include()
rules = yara.compile(filepath=YARA_RULES)
for file in os.listdir(DATA_DIR):
    file_path_abs = os.path.join(DATA_DIR, file)
    if os.path.isdir(file_path_abs):
        continue
    rules.match(file_path_abs, callback=wrap_callback(file_path_abs, family_dispatch_map),
                which_callbacks=yara.CALLBACK_MATCHES)


def dispatcher(shell_family, maps: Dict):
    for family_name, data_dict in maps.items():
        if family_name not in current_ability:
            continue
        worker = shell_family.get(family_name)
        print(family_name, len(data_dict.values()))
        try:
            worker.do(data_dict)
        except:
            print("Error happened when processing {}".format(family_name))


if __name__ == '__main__':
    sf = ShellFamily()
    sf.initialize()

    dispatcher(sf, family_dispatch_map)
