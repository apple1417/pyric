import functools
import re
import subprocess
from pathlib import Path

from . import assets

LIST_PRESETS_RE = re.compile('  "(.+)"')


@functools.cache
def cmake_get_presets() -> list[str]:
    """
    Gets the presets which may be used.

    Returns:
        A list of presets.
    """
    proc = subprocess.run(
        ["cmake", "--list-presets"],
        cwd=assets.ASSETS_PATH,
        check=True,
        stdout=subprocess.PIPE,
        encoding="utf8",
    )
    return LIST_PRESETS_RE.findall(proc.stdout)


def cmake_configure(working_dir: Path, preset: str, extra_args: list[str]) -> None:
    """
    Configures CMake.

    Args:
        working_dir: The working dir to configure in.
        preset: The preset to configure with.
        extra_args: Extra args to pass to CMake.
    """
    for build_type in ("Debug", "Release"):
        build_dir = working_dir / build_type.lower()
        (build_dir / "CMakeCache.txt").unlink(missing_ok=True)

        subprocess.run(
            [
                "cmake",
                working_dir,
                "-B",
                build_dir,
                "--preset",
                preset,
                f"-DCMAKE_BUILD_TYPE={build_type}",
                *extra_args,
            ],
            check=True,
        )


def cmake_build(working_dir: Path, release: bool) -> Path:
    """
    Performs a build.

    Args:
        working_dir: The working dir to build.
        release: True if to make a release build, false if to make a debug.
    Returns:
        The path of the built target.
    """

    build_dir = working_dir / ("release" if release else "debug")

    subprocess.run(["cmake", "--build", build_dir], check=True)

    return build_dir / ("pyric.pyd" if release else "pyric_d.pyd")
