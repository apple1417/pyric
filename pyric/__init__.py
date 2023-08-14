import argparse
from pathlib import Path


def path_arg(input_path: str) -> Path:
    """
    Parses a path argument.

    Fully resolves the path before returning.

    Args:
        input_path: The input path to convert.
    Returns:
        The converted + resolved path.
    """
    return Path(input_path).resolve()


def file_arg(input_path: str) -> Path:
    """
    Parses an argument which should be a file.

    Args:
        input_path: The input path to check.
    Returns:
        The file converted to a path, if valid.
    """
    out = path_arg(input_path)
    if out.exists() and out.is_file():
        return out
    raise argparse.ArgumentTypeError(f"'{input_path}' is not a valid file")


def directory_arg(input_path: str) -> Path:
    """
    Parses an argument which should be a directory.

    Args:
        input_path: The input path to check.
    Returns:
        The directory converted to a path, if valid.
    """
    out = path_arg(input_path)
    if out.exists() and out.is_dir():
        return out
    raise argparse.ArgumentTypeError(f"'{input_path}' is not a valid directory")
