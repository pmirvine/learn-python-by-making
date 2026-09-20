import platform


def main():
    print(f"Python {platform.python_version()} Computer")
    print()
    print(f"{platform.system()} {platform.machine()}")
    print()
    print("Ready")
    print(">")


if __name__ == "__main__":
    main()
