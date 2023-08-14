import argparse

from .build import add_build_subcommand, run_build_subcommand
from .init import add_init_subcommand, run_init_subcommand


def main() -> None:
    """Main entry point."""

    parser = argparse.ArgumentParser(
        "pyric",
        description="Helper to build simple pyunrealsdk extensions.",
    )
    subparsers = parser.add_subparsers(help="Sub-command help.", dest="subcommand")

    add_init_subcommand(
        subparsers.add_parser(
            "init",
            description="Initializes a new pyric working dir.",
        ),
    )

    add_build_subcommand(
        subparsers.add_parser(
            "build",
            description="Builds an extension.",
        ),
    )

    subcommand_runners = {
        "init": run_init_subcommand,
        "build": run_build_subcommand,
    }

    args = parser.parse_args()
    subcommand_runners[args.subcommand](args)


if __name__ == "__main__":
    main()
