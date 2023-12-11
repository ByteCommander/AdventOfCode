# small library with commonly needed helpers for the daily challenges,
# including a generic main/test executor which handles input files and test strings automatically.

import __main__
from collections.abc import Callable
from io import StringIO
from pathlib import Path
from typing import TextIO


def run(main: Callable[[TextIO], None], test_input: str = None, test_only: bool = False) -> None:
    """
    Run the provided challenge main function, first with test input, then with real input.
    The input file to use gets discovered automatically based on the calling module file name.
    :param main: challenge main function to call, must accept a file-like parameter for the input
    :param test_input: test input as plain text string
    :param test_only: set to true to run only the test and ignore the real input file (for debugging)
    """
    if test_input:
        print("*** TEST ***")
        main(StringIO(test_input.strip("\n")))

    if test_input and not test_only:
        print("\n*** REAL ***")

    if not test_only:
        script_path = Path(__main__.__file__)
        input_path = script_path.parent / "inputs" / (script_path.name.removesuffix(".py")[:-1] + ".txt")
        with open(input_path) as file:
            main(file)
