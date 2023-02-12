from . import APP_NAME, APP_DESCRIPTION
from argparse import ArgumentParser


def main():
    parser = ArgumentParser(prog=APP_NAME, description=APP_DESCRIPTION)
    parser.add_argument(
        "--device",
        "-d",
        dest="device",
        type=str,
        default="/dev/ttyS0",
        help="Path to power supply device.",
    )
    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    main()
