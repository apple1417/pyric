from pathlib import Path

ASSETS_PATH: Path = Path(__file__).resolve().parent

CMAKELISTS: Path = ASSETS_PATH / "CMakeLists.txt"
CMAKEPRESETS: Path = ASSETS_PATH / "CMakePresets.json"

COMMON_CMAKE: Path = ASSETS_PATH / "common_cmake"
