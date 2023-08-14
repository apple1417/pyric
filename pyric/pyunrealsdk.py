import subprocess
import sys
from pathlib import Path

from .assets.common_cmake.explicit_python.download import ARCHITECTURES, download

PYUNREALSDK_GIT_URL_SSH: str = "git@github.com:bl-sdk/pyunrealsdk.git"
PYUNREALSDK_GIT_URL_HTTP: str = "https://github.com/bl-sdk/pyunrealsdk.git"


def update_pyunrealsdk_py_version(pyunrealsdk_dir: Path, py_version: str) -> None:
    """
    Updates the python version which a pyunrealsdk install is linking against.

    Args:
        pyunrealsdk_dir: The directory holding pyunrealsdk.
        py_version: The python version to download, or None to use that of the current interpreter.
    """
    explicit_py_folder = pyunrealsdk_dir / "common_cmake" / "explicit_python"

    # Install all architectures, so that if this is used as a symlink we're already ready for other
    # configurations
    for arch in ARCHITECTURES:
        download(py_version, arch, False, True, explicit_py_folder / arch.folder_name)


def clone_pyunrealsdk(
    working_dir: Path,
    pyunrealsdk_source: Path | None,
    py_version: str | None,
) -> None:
    """
    Clones pyunrealsdk.

    Args:
        working_dir: The working dir to clone into.
        pyunrealsdk_source: Another path to try copy from, or None if to clone from git.
        py_version: If cloning from git, the python version to initialize to, or None to use that of
                    the current interpreter.
    """
    pyunrealsdk_dest = working_dir / "pyunrealsdk"

    # Only get a new copy of pyunrealsdk if one doesn't already exist, don't overwrite
    if not pyunrealsdk_dest.exists():
        if pyunrealsdk_source is None:
            try:
                subprocess.run(
                    ["git", "clone", "--recursive", PYUNREALSDK_GIT_URL_SSH, pyunrealsdk_dest],
                    check=True,
                )
            except subprocess.CalledProcessError:
                # If an ssh clone fails, try again with http
                subprocess.run(
                    ["git", "clone", "--recursive", PYUNREALSDK_GIT_URL_HTTP, pyunrealsdk_dest],
                    check=True,
                )

            # Since we're on a fresh clone and don't have anything, force a version update
            if py_version is None:
                py_version = ".".join(str(x) for x in sys.version_info[:3])
        else:
            if (inner_dir := (pyunrealsdk_source / "pyunrealsdk")).exists() and inner_dir.is_dir():
                pyunrealsdk_source = inner_dir

            pyunrealsdk_dest.symlink_to(pyunrealsdk_source, target_is_directory=True)

    # Update version if we've been asked to
    if py_version is not None:
        update_pyunrealsdk_py_version(pyunrealsdk_dest, py_version)
