import argparse
import shutil
from pathlib import Path

from . import assets, directory_arg, path_arg
from .cmake import cmake_build, cmake_configure, cmake_get_presets
from .pyunrealsdk import clone_pyunrealsdk


def add_init_subcommand(parser: argparse.ArgumentParser) -> None:
    """
    Adds all the arguments for the init sub command.

    Args:
        parser: The parser to add commands to.
    """
    parser.add_argument("preset", choices=cmake_get_presets(), help="Which preset to use.")
    parser.add_argument("cmake_args", nargs="*", help="Extra args to pass to the CMake configure.")

    parser.add_argument(
        "-d",
        "--dir",
        default=".pyric",
        type=path_arg,
        help="Directory to install into.",
    )
    parser.add_argument(
        "-p",
        "--py-version",
        default=None,
        help=(
            "The python version to download the dev files for. If not given uses the existing"
            " files, or the version of the current interpreter if on a fresh pyunrealsdk download."
            " If run against an existing install, overwrites it's version."
        ),
    )

    parser.add_argument(
        "--pyunrealsdk",
        type=directory_arg,
        help=(
            "Rather than downloading a new copy of pyunrealsdk from github, symlink from the given"
            " path. May be given a working dir to copy it's install, or the pyunrealsdk dir itself."
        ),
    )


def run_init_subcommand(args: argparse.Namespace) -> None:
    """
    Runs an init sub command.

    Args:
        args: The parsed args.
    """
    working_dir: Path = args.dir

    working_dir.mkdir(parents=True, exist_ok=True)

    (working_dir / ".gitignore").open("w").write("*")

    src_dir = working_dir / "src"
    src_dir.mkdir(parents=True, exist_ok=True)
    for old_file in src_dir.iterdir():
        if old_file.is_file():
            old_file.unlink()

    clone_pyunrealsdk(working_dir, args.pyunrealsdk, args.py_version)

    shutil.copy(assets.CMAKELISTS, working_dir)
    shutil.copy(assets.CMAKEPRESETS, working_dir)

    working_cmake_common = working_dir / assets.COMMON_CMAKE.name
    if not working_cmake_common.exists():
        working_cmake_common.symlink_to(assets.COMMON_CMAKE, target_is_directory=True)

    cmake_configure(working_dir, args.preset, args.cmake_args)

    # Pre-build with no sources, to speed up later builds
    cmake_build(working_dir, True)
    cmake_build(working_dir, False)
