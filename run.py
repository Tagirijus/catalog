"""
Programm for analyzing an ODS spreadsheet.

The program takes a file as argument (ODS file) and loads its columns
and rows into the database. Then you can filter and search things.
"""

import argparse
from modules import catalog


# get arguments
ARGS = argparse.ArgumentParser(
    description=(
        'Programm for analysing a ODS spreadsheet.'
    )
)

ARGS.add_argument(
    'file',
    nargs='?',
    default=None,
    help=(
        'ODS file'
    )
)

ARGS = ARGS.parse_args()

if __name__ == '__main__':
    DB = catalog.Catalog(file=ARGS.file)
