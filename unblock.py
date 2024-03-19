import os
import sys
from typing import *

import psutil

cwd = os.path.dirname(os.path.realpath(__file__))
hosts_location = r"C:\Windows\System32\drivers\etc\hosts"
block_format = "\n127.0.0.1 %s"


def unblock_sites(urls: List[str]) -> None:
    """
    Unblock a given list of urls by removing them from the hosts file.

    :param urls: The list of urls to unblock.
    :return:
    """
    with open(hosts_location, "r+") as hosts:
        lines = hosts.readlines()
        hosts.seek(0)
        for line in lines:
            if (not any(site in line for site in urls)) and bool(line.strip()):
                hosts.write(line)
        hosts.truncate()


def kill_py():
    for process in psutil.process_iter():
        if "pythonw" in process.name():
            try:
                process.kill()
            except Exception:  # noqa
                os.system("taskkill /f /im " + process.name() + " >nul")


if __name__ == '__main__':
    with open(cwd + "\\blocked_sites.txt", "r") as f:
        blocked_sites = [x.rstrip() for x in f.read().splitlines()]

    kill_py()
    unblock_sites(blocked_sites)

    sys.exit()
