"""Compare two JSON files while ignoring values of the description key."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def values_match(first: Any, second: Any, path: str = "root") -> tuple[bool, str]:
    """Return whether two JSON values match and describe the first mismatch."""
    if isinstance(first, dict) or isinstance(second, dict):
        if not isinstance(first, dict) or not isinstance(second, dict):
            return False, f"{path}: different JSON types"

        first_keys = set(first)
        second_keys = set(second)
        missing_keys = first_keys - second_keys
        extra_keys = second_keys - first_keys
        if missing_keys:
            key = sorted(missing_keys)[0]
            return False, f"{path}: missing key {key}"
        if extra_keys:
            key = sorted(extra_keys)[0]
            return False, f"{path}: unexpected key {key}"

        for key in first:
            if key == "description":
                continue
            matches, mismatch = values_match(first[key], second[key], f"{path}.{key}")
            if not matches:
                return False, mismatch
        return True, ""

    if isinstance(first, list) or isinstance(second, list):
        if not isinstance(first, list) or not isinstance(second, list):
            return False, f"{path}: different JSON types"
        if len(first) != len(second):
            return False, f"{path}: different list lengths"
        for index, (first_item, second_item) in enumerate(zip(first, second, strict=True)):
            matches, mismatch = values_match(first_item, second_item, f"{path}[{index}]")
            if not matches:
                return False, mismatch
        return True, ""

    if type(first) is not type(second):
        return False, f"{path}: different JSON types"
    if first != second:
        return False, f"{path}: different values"
    return True, ""


def load_json(file_path: Path) -> Any:
    """Load one UTF-8 JSON file."""
    with file_path.open(encoding="utf-8") as json_file:
        return json.load(json_file)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two JSON files and ignore description values.")
    parser.add_argument("first_file", type=Path, help="Path to the first JSON file")
    parser.add_argument("second_file", type=Path, help="Path to the second JSON file")
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    try:
        first_json = load_json(arguments.first_file)
        second_json = load_json(arguments.second_file)
    except (OSError, json.JSONDecodeError):
        print("ERROR: Could not read valid UTF-8 JSON input.")
        return 2

    matches, mismatch = values_match(first_json, second_json)
    if matches:
        print("MATCH: JSON files are equal except for description values.")
        return 0

    print("DIFFERENCE: JSON files are not equal outside description values.")
    print(f"Location: {mismatch}".encode("ascii", "backslashreplace").decode("ascii"))
    return 1


if __name__ == "__main__":
    sys.exit(main())
