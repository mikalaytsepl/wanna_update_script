import os
import subprocess as sub


def check_for_upgrades() -> bool:
    test = sub.run(["sudo", "apt", "update"], capture_output=True, text=True).stdout

    manager_status = test.splitlines()[-1]

    if manager_status != "All packages are up to date.":
        print(f"There are {manager_status.split()[0]} packages to upgrade")
        what_exactly = sub.run(
            ["sudo", "apt", "list", "--upgradable"], capture_output=True, text=True
        ).stdout
        print(what_exactly)


def parse_package_list(packlist: str):
    pass  # make parsing logic here


while True:
    choice = input(f'Hi, {os.getenv("USER")}! Want to check for any updates?\nY/N:')
    match choice:
        case "Y" | "y":
            print("Updating packages information...")
            check_for_upgrades()
            break
        case "N" | "n":
            print("Update proposition declined.")
            break
        case _:
            print("Please, specify only Y(y) or N(n).")
