import os
import sys
import time
from datetime import datetime, timedelta
from typing import *

import psutil

cwd = os.path.dirname(os.path.realpath(__file__))
hosts_location = r"C:\Windows\System32\drivers\etc\hosts"
block_format = "\n127.0.0.1 %s"
block_seconds = 60 * 60


def block_sites(urls: List[str]) -> None:
    """
    Block a given list of urls by adding them to the hosts file.

    :param urls: List of urls to block.
    """
    with open(hosts_location, "a") as hosts:
        for url in urls:
            block_site(hosts, url)


def block_site(file, url: str) -> None:
    """
    Add a given url to the hosts file.

    :param file: The hosts file.
    :param url: The URL to block.
    :return:
    """
    file.write(block_format % url)

    if not url.startswith("www."):
        file.write(block_format % f"www.{url}")


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
            if not any(site in line for site in urls):
                hosts.write(line)
        hosts.truncate()


def close_blocked_apps(apps: List[str]) -> List[psutil.Process]:
    """
    Close any running processes that match the given list of apps.

    :param apps: The list of blocked apps.
    :return: The apps that were closed.
    """
    blocked = []

    for process in psutil.process_iter():
        if any(app.lower() in process.name().lower() for app in apps):
            blocked.append(process)
            try:
                process.kill()
            except Exception:  # noqa
                os.system("taskkill /f /im " + process.name() + " >nul")

    return blocked


if __name__ == '__main__':

    with open(cwd + "\\blocked_sites.txt", "r") as f:
        blocked_sites = [x.rstrip() for x in f.read().splitlines()]

    with open(cwd + "\\blocked_apps.txt", "r") as f:
        blocked_apps = [x.rstrip() for x in f.read().splitlines()]

    try:
        now = datetime.now()
        end = now + timedelta(seconds=block_seconds)

        block_sites(blocked_sites)
        os.system("ipconfig /flushdns >nul")  # Required for sites like YouTube

        while datetime.now() < end:
            close_blocked_apps(blocked_apps)
            time.sleep(10)

        sys.exit()
    except:
        raise
    finally:
        unblock_sites(blocked_sites)