import datetime
import os
import sys
from pathlib import Path
from string import Template

import requests
from dotenv import load_dotenv

ENV_COOKIE_NAME = "AOC_SESSION_COOKIE"
AOC_INPUT_URL_PATTERN = "https://adventofcode.com/{year}/day/{day}/input"
TOOL_DIR = Path(__file__).parent
BASE_DIR = TOOL_DIR.parent
PARTS = ["", "a", "b"]


def main():
    if len(sys.argv) not in (3, 1):
        print("Error! Expected exactly two integer arguments.")
        print("Usage:   {} <YEAR> <DAY>".format(sys.argv[0]))
        exit(1)

    if len(sys.argv) == 3:
        _, year, day = sys.argv
    else:
        year = input("Year: ")
        day = input("Day:  ")

    template_solution(year, day)
    download(year, day)


def template_solution(year: int, day: int, part: int = 1) -> None:
    date = datetime.date.today().isoformat()
    path = BASE_DIR / str(year) / f"aoc{year}_{day}{PARTS[part]}.py"

    if path.exists():
        print(f"WARNING: file {path} already exists, not overwriting with template!")
        return

    with open(TOOL_DIR / "_template.py") as tpl_file:
        tpl = Template(tpl_file.read())

    with open(path, "w") as out_file:
        out_file.write(tpl.substitute(year=year, day=day, date=date, part=part))
    print(f"Created solution template file for day {day} ({year}) as {path}")


def download(year: int, day: int) -> None:
    path = BASE_DIR / str(year) / "inputs" / f"aoc{year}_{day}.txt"
    url = AOC_INPUT_URL_PATTERN.format(year=year, day=day)

    if not (cookie := _get_cookie()):
        return

    response = requests.get(url, cookies={"session": cookie})
    if response.ok:
        with open(path, "w") as file:
            file.write(response.text)
        print(f"Downloaded input file for day {day} ({year}) and saved {len(response.text)} bytes as {path}")

    else:
        print(f"ERROR: Request to {url} failed (status {response.status_code} - {response.reason})")
        print(response.text)


def _get_cookie() -> str|None:
    load_dotenv()
    if cookie := os.getenv(ENV_COOKIE_NAME):
        return cookie

    # deprecated old txt file
    txt_path = BASE_DIR / "session-cookie.txt"
    if txt_path.exists():
        with open(txt_path)as txt_file:
            if cookie := txt_file.read().strip():
                return cookie

    print(f"ERROR: no authentication cookie value found in {ENV_COOKIE_NAME} env var or .env file!")
    print("Please copy the 'session' cookie from your logged in adventofcode.com browser session.")

if __name__ == "__main__":
    main()
