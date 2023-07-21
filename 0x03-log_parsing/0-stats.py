#!/usr/bin/python3
"""
This is the `0-stats` module. It is meant to be a log parser.
"""
import re
from typing import Dict


# total_size is the total size of all the files processed.
total_size = 0

# status_code_dict is a dictionary of the status codes and their count
# across all files. The status codes are used as keys, and their count values.
status_code_dict = {
    200: 0, 301: 0, 400: 0, 401: 0, 403: 0, 404: 0, 405: 0, 500: 0,
}

# pp are the pattern parts.
pp = (
    r'^\b(?:\d{1,3}\.){3}\d{1,3}\b',
    r'\s-\s',
    r'\[.+\]\s',
    r'"GET /projects/260 HTTP/1\.1"\s',
    r'(?P<status_code>\d{3}) (?P<file_size>\d+)$'
)
# line_pattern is the regex pattern to match the lines in the files.
line_pattern = re.compile(
    '{}{}{}{}{}'.format(pp[0], pp[1], pp[2], pp[3], pp[4])
)


def print_stats(total_size: int, status_code_dict: Dict) -> None:
    """
    print_stats prints the stats.
    """
    print("File size: {}".format(total_size), flush=True)
    for status_code, count in sorted(status_code_dict.items()):
        if count == 0:
            continue
        print("{}: {}".format(status_code, count), flush=True)


def compute_stats(line_no: int, line: str) -> None:
    """
    compute_stats keeps track of the total size and the count of each
    status code.
    """
    try:
        match = line_pattern.match(line)
        if not match:
            return

        status_code = int(match.group("status_code"))
        file_size = int(match.group("file_size"))
        if status_code not in status_code_dict:
            return

        global total_size
        total_size += file_size

        status_code_dict[status_code] = status_code_dict.get(
            status_code, 0) + 1

        if line_no % 10 == 0:
            print_stats(total_size, status_code_dict)
    except ValueError:
        return


def parse_lines() -> None:
    """
    parse_lines parses each line in the logs and computes the stats.
    """
    global total_size
    try:
        line_no = 0
        while True:
            line = input()
            line_no += 1
            compute_stats(line_no, line)
    except (KeyboardInterrupt, EOFError):
        print_stats(total_size, status_code_dict)


if __name__ == "__main__":
    parse_lines()
