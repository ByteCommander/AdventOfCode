import sys

import os
from bs4 import BeautifulSoup
import requests
from getpass import getpass

AOC_AUTH_URL = "https://adventofcode.com/auth/github"
GITHUB_LOGIN_URL = "https://github.com/session"
CLIENT_ID = "7bb0a7ec13388aa67963"


# def printhtml(html):
#     soup = BeautifulSoup(html, "lxml")
#     for tag in soup('script'):
#         tag.extract()
#     print("\n".join(
#         line.rstrip() for line in soup.text.splitlines() if line.strip()))
#
#
# def printresp(resp: requests.Response):
#     print(resp, resp.reason, resp.url)
#     print("-----")
#     print(*resp.headers.items(), sep="\n")
#     print("-----")
#     print(*resp.cookies.items(), sep="\n")
#     print("-----")
#     printhtml(resp.text)


def get_cookie():
    try:
        with open(os.path.join(os.path.dirname(__file__),
                               "../session-cookie.txt")) as file:
            cookie = file.read().strip()
            if not cookie:
                raise ValueError("File 'session-cookies.txt' is empty.")

    except (ValueError, IOError) as e:
        print(e)
        print("No valid cookie stored locally, authenticating online...")
        cookie = login_with_github()

    return cookie


def store_cookie(cookie):
    with open(os.path.join(os.path.dirname(__file__),
                           "../session-cookie.txt"), "w") as file:
        file.write(cookie)


def login_with_github():
    response = requests.get(AOC_AUTH_URL)
    soup = BeautifulSoup(response.text, "lxml")
    a_token = soup.find("input", {"name": "authenticity_token"}).get("value")
    github_temp_sess_cookie = response.cookies.get("_gh_sess")

    github_email, github_password = get_credentials("GitHub")

    with requests.session() as session:
        session.post(GITHUB_LOGIN_URL,
                     data={
                         "login": github_email,
                         "password": github_password,
                         "authenticity_token": a_token
                     },
                     cookies={"_gh_sess": github_temp_sess_cookie})
        aoc_session_cookie = session.cookies.get(name="session",
                                                 domain=".adventofcode.com")

    store_cookie(aoc_session_cookie)
    return aoc_session_cookie


def get_credentials(provider_name):
    print("*** Sign in to AdventOfCode.com using {} ***".format(provider_name),
          file=sys.stderr)
    print("Email address: ", file=sys.stderr, end="")
    email = input()
    password = getpass("Password:      ", sys.stderr)
    return email, password


if __name__ == "__main__":
    print("Your Advent Of Code session cookie is:", get_cookie())
