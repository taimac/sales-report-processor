from __future__ import annotations

from pathlib import Path
import re
from typing import Any


TIMESTAMP_PATTERN = re.compile(
    r"(?P<date>\d{2}/\d{2}/\d{4})\s*-\s*(?P<time>\d{2}:\d{2}:\d{2})"
)


def read_txt_report(file_path: str | Path) -> dict[str, Any]:
    """
    Read a TXT report safely, normalize line endings, preserve raw text,
    and extract generated date/time metadata.
    """
    path = Path(file_path)
    raw_bytes = path.read_bytes()

    try:
        raw_text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raw_text = raw_bytes.decode("latin-1")

    normalized_text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.replace("\x0c", "").rstrip() for line in normalized_text.split("\n")]

    metadata = extract_generated_datetime(lines)

    return {
        "raw_text": raw_text,
        "lines": lines,
        "metadata": metadata,
    }


def extract_generated_datetime(lines: list[str]) -> dict[str, str | None]:
    """
    Extract report generated date and time from the header area.
    Returns None values if not found.
    """
    for line in lines:
        match = TIMESTAMP_PATTERN.search(line)
        if match:
            return {
                "generated_date": match.group("date"),
                "generated_time": match.group("time"),
            }

    return {
        "generated_date": None,
        "generated_time": None,
    }