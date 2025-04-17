import plistlib
import re
from typing import Annotated

import requests
import typer
import yaml

app = typer.Typer()

TagGroups = dict[str, list[dict[str, str]]]

# Reserved tag to catch all numbers
ALL_GROUP_TAG = "all"

# Category used by Begone for blocked numbers
CATEGORY_BLOCKED = "0"

# French phone number format
FRENCH_NUMBER_FORMAT = "+33 {1} {2} {3} {4} {5}"

# Regex to match French phone numbers with optional country code
FRENCH_NUMBER_REGEX = re.compile(
    r"^(\+33|0)([0-9#])([0-9#]{2})([0-9#]{2})([0-9#]{2})([0-9#]{2})$"
)


def sanitize_number(number: str) -> str:
    return re.sub(r"[^+0-9#]", "", number)


def format_number(number: str) -> str:
    if not (match := FRENCH_NUMBER_REGEX.match(number)):
        raise ValueError(f"Invalid phone number: {number}")
    return FRENCH_NUMBER_FORMAT.format(*match.groups())


def find_common_prefix(strings: list[str]) -> str:
    if not strings:
        return ""

    prefix = strings[0]
    for s in strings[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix


def entry_to_pattern(entry: dict[str, str]) -> str:
    prefix = find_common_prefix([
        entry["Tranche_Debut"],
        entry["Tranche_Fin"],
    ])
    pattern = prefix.ljust(10, "#")
    return format_number(pattern)


def fetch_number_ranges(mnemonic: str) -> list[str]:
    url = (
        f"https://tabular-api.data.gouv.fr/api/resources"
        f"/90e8bdd0-0f5c-47ac-bd39-5f46463eb806"
        f"/data/?Mn%C3%A9mo__exact={mnemonic}"
    )

    numbers: list[str] = []
    while url:
        r = requests.get(url, timeout=10)
        r.raise_for_status()

        data = r.json()
        numbers.extend(entry_to_pattern(entry) for entry in data["data"])

        url = data["links"]["next"]
    return sorted(numbers)


def load_numbers(input_file: str) -> TagGroups:
    with open(input_file) as f:
        entries = yaml.safe_load(f)

    groups: TagGroups = {}
    for entry in entries:
        numbers = entry.get("numbers", [])
        mnemonic = entry.get("mnemonic")
        if mnemonic:
            numbers.extend(fetch_number_ranges(mnemonic))

        group = []
        for number in numbers:
            group.append({
                "title": entry["title"],
                "addNational": "true",
                "category": CATEGORY_BLOCKED,
                "number": sanitize_number(number),
            })

        for tag in entry.get("tags", []):
            if tag == ALL_GROUP_TAG:
                continue
            groups.setdefault(tag, []).extend(group)
        groups.setdefault(ALL_GROUP_TAG, []).extend(group)

    return groups


def main(
    input_file: Annotated[str, typer.Argument(help="Input YAML numbers file")],
    output_file: Annotated[str, typer.Argument(help="Output Begone XML file")],
    tags: Annotated[list[str], typer.Argument(help="Tags to include")],
) -> None:
    groups = load_numbers(input_file)
    output = []
    for tag in tags:
        output.extend(groups.get(tag, []))

    with open(output_file, "wb") as f:
        plistlib.dump(output, f)


def run() -> None:
    typer.run(main)


if __name__ == "__main__":
    run()
