"""
Programm for analyzing an ODS spreadsheet.

The program takes a file as argument (ODS file) and loads its columns
and rows into the database. Then you can filter and search things.
"""

import argparse
from modules import catalog
from modules import settings


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

ARGS.add_argument(
    '-f',
    '--force-convert',
    action='store_true',
    help='Force converting to DB.pkl'
)

ARGS.add_argument(
    '-d',
    '--default',
    default=None,
    metavar='JSON file',
    help='Create JSON file holding the default columns for the database'
)

ARGS.add_argument(
    '-c',
    '--columns',
    default=None,
    metavar='JSON file',
    help='JSON file holding the columns for the database'
)

ARGS = ARGS.parse_args()

if __name__ == '__main__':
    # initialize SETTINGS
    SETTINGS = settings.Settings(
        columns_file=ARGS.columns,
        force_convert=ARGS.force_convert
    )

    # get default columns, if parameter is set
    if ARGS.default is not None:
        SETTINGS.dump_default_columns_to_file(
            file=ARGS.default
        )
        exit()

    # initialize DB
    DB = catalog.Catalog(
        file=ARGS.file,
        settings=SETTINGS
    )