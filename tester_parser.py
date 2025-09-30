import os
import subprocess as sub
import re
from tabulate import tabulate
import sys


def check_for_upgrades() -> bool:
    test = sub.run(["sudo", "apt", "update"], capture_output=True, text=True).stdout

    manager_status = test.splitlines()[-1]

    if manager_status != "All packages are up to date.":
        print(f"There are {manager_status.split()[0]} packages to upgrade")
        return True
    else:
        print("No candidates for upgrade found.")
        return False


def parse_package_list() -> list[dict]:
    upgd_list = sub.run(
        ["sudo", "apt", "list", "--upgradable"], capture_output=True, text=True
    ).stdout
    splitted_upgd_list = upgd_list.splitlines()[1:]

    package_information = []

    for line in splitted_upgd_list:
        # versions = re.findall(r"(?:[0-9]+)+(?:\.[0-9]+)+", line)

        name = re.search(r"^.+(?=\/)", line).group()

        toblock = line.split()[1]
        fromblock = line.split()[-1]
        from_version = re.search(r"(.*?)(?=]$)", fromblock).group()

        package_information.append(
            {
                "name": name,
                "upgrade_to_version": toblock,
                "upgrade_from_version": from_version,
            }
        )

    return package_information


def create_table(packages):
    print(tabulate(packages, headers="keys"))


def upgrade_stuff():
    while True:
        choice = input(f"Proceed to upgrade?\nY/N:")
        match choice:
            case "Y" | "y":
                print(
                    "Great, packages are now upgrading"
                )  # how to make at least that 3 dots loading thing
                sub.run(["sudo", "apt", "upgrade"])
                break
            case "N" | "n":
                print("Upgrade discarded.")
                break
            case _:
                print("Please, specify only Y(y) or N(n).")


if sys.stdin.isatty():
    while True:
        choice = input(f'Hi, {os.getenv("USER")}! Want to check for any updates?\nY/N:')
        match choice:
            case "Y" | "y":
                print("Checking for upgrades...")
                if check_for_upgrades():
                    packlist = parse_package_list()
                    create_table(packlist)
                    upgrade_stuff()
                break
            case "N" | "n":
                print("Update proposition declined.")
                break
            case _:
                print("Please, specify only Y(y) or N(n).")
else:
    sys.exit(0)
