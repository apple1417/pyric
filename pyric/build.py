import argparse
import shutil
from pathlib import Path

from . import directory_arg, file_arg, path_arg
from .cmake import cmake_build


def add_build_subcommand(parser: argparse.ArgumentParser) -> None:
    """
    Adds all the arguments for the build sub command.

    Args:
        parser: The parser to add commands to.
    """

    parser.add_argument(
        "-d",
        "--dir",
        default=".pyric",
        type=directory_arg,
        help="Working directory to use.",
    )

    parser.add_argument("files", nargs="*", type=file_arg, help="The file(s) to compile.")

    parser.add_argument(
        "-o",
        "--output",
        type=path_arg,
        help="The output file to write to. Debug builds automatically add the `_d` suffix.",
    )

    parser.add_argument("--debug", action="store_true", help="Compile a debug build.")
    parser.add_argument(
        "--release",
        action="store_true",
        help="Compile a release build. The default.",
    )


def sync_build_files(working_dir: Path, files: list[Path]) -> None:
    """
    Syncs the build files into the working dir, with as few file modifications as possible.

    Args:
        working_dir: The working dir to build within.
        files: The files to sync.
    """
    src_dir = working_dir / "src"

    # Look for any files we need to delete
    for file in src_dir.iterdir():
        if not file.is_file():
            continue

        # If the file is a symlink pointing to something we're meant to copy
        resolved = file.resolve()
        if resolved in files:
            # Don't copy it
            files.remove(resolved)
            # Don't delete it
            continue

        file.unlink()

    # Symlink the remaining files
    for file in files:
        (src_dir / file.name).symlink_to(file)


def run_build_subcommand(args: argparse.Namespace) -> None:
    """
    Runs a build sub command.

    Args:
        args: The parsed args.
    """
    working_dir: Path = args.dir

    files: list[Path] = args.files
    output: Path = files[0].with_suffix(".pyd") if args.output is None else args.output

    debug: bool = args.debug
    release: bool = args.release
    if not args.debug and not args.release:
        release = True

    sync_build_files(working_dir, files)

    if release:
        release_target = cmake_build(working_dir, True)
        shutil.copy(release_target, output)

    if debug:
        debug_output = output.with_stem(output.stem + "_d")
        debug_target = cmake_build(working_dir, False)
        shutil.copy(debug_target, debug_output)
