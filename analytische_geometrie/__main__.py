import argparse
from . import __version__


def main():
    parser = argparse.ArgumentParser(
        prog="analytische_geometrie",
        description="Bibliothek für analytische Geometrie in 3D."
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    parser.parse_args()


if __name__ == "__main__":
    main()