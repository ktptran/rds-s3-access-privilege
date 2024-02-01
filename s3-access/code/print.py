#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Print JSON data.

Prints out the data collected from our different scripts to the user
"""

import os

def main():
    files = os.listdir('./Data/')
    for file_name in files:
        print(f"{file_name}")
        print_json(file_name)
        print()


def print_json(input_file):
    """
    Print the given input file text to the user.

    Parameters
    ----------
    input_file: string
        File name to print from data collected.
    """
    file_log = open(f"./Data/{input_file}", "r").read()
    print(file_log)


if __name__ == '__main__':
    main()
