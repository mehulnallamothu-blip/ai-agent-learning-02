"""Read the contents of a local text file."""

from pathlib import Path


def read_text_file(path: str) -> str:
    """Return the UTF-8 contents of a local text file."""
    if not path or not path.strip():
        raise ValueError("A file path is required.")

    file_path = Path(path).expanduser()
    if not file_path.is_file():
        raise ValueError(f"File not found: {file_path}")

    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"File is not valid UTF-8 text: {file_path}") from error
    except OSError as error:
        raise ValueError(f"Could not read file: {error}") from error
