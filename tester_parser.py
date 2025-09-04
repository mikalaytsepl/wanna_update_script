import os
import subprocess as sub
import re


def check_for_upgrades() -> bool:
    test = sub.run(["sudo", "apt", "update"], capture_output=True, text=True).stdout

    manager_status = test.splitlines()[-1]

    if manager_status != "All packages are up to date.":
        print(f"There are {manager_status.split()[0]} packages to upgrade")
        return True
    else:
        return False


def parse_package_list() -> list[dict]:
    upgd_list = sub.run(
        ["sudo", "apt", "list", "--upgradable"], capture_output=True, text=True
    ).stdout
    splitted_upgd_list = upgd_list.splitlines()[1:]
    package_information = [
        {
            "name": re.search(r"^.+(?=\/)", line).group(),
            "to_version": versions[0] if len(versions) > 0 else None,
            "from_version": versions[1] if len(versions) > 1 else None,
        }
        for line in splitted_upgd_list
        for versions in [re.findall(r"(?:[0-9]+\.){2}[0-9]+", line)]
    ]
    return package_information


while True:
    choice = input(f'Hi, {os.getenv("USER")}! Want to check for any updates?\nY/N:')
    match choice:
        case "Y" | "y":
            print("Updating packages information...")
            if check_for_upgrades():
                parse_package_list()
            break
        case "N" | "n":
            print("Update proposition declined.")
            break
        case _:
            print("Please, specify only Y(y) or N(n).")
