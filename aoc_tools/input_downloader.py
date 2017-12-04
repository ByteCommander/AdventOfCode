import os
import sys
import requests
from bs4 import BeautifulSoup

import authenticator

AOC_INPUT_URL_PATTERN = "https://adventofcode.com/{year}/day/{day}/input"


def main():
    if len(sys.argv) not in (3, 1):
        print("Error! Expected exactly two integer arguments.")
        print("Usage:   {} <YEAR> <DAY>".format(sys.argv[0]))
        exit(1)

    if len(sys.argv) == 3:
        script_name, year, day = sys.argv
    else:
        year = input("Year: ")
        day = input("Day:  ")
    created_file, size = download(year, day)

    print("Downloaded input file for day {} ({}) and saved {} bytes as {}"
          .format(day, year, size, created_file))


def download(year, day):
    filename = os.path.join(os.path.dirname(__file__), "..", str(year),
                            "inputs", "aoc{}_{}.txt".format(year, day))
    url = AOC_INPUT_URL_PATTERN.format(year=year, day=day)

    cookie = authenticator.get_cookie()
    response = requests.get(url, cookies={"session": cookie})
    if response.ok:
        with open(filename, "w") as file:
            file.write(response.text)
        return filename, len(response.text)
    else:
        print("Error! Request to {} failed (status {} - {})"
              .format(url, response.status_code, response.reason))
        soup = BeautifulSoup(response.text)
        for tag in soup("script"):
            tag.extract()
        print(soup.text)
        response.raise_for_status()


if __name__ == "__main__":
    main()
