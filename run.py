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
    '-F',
    '--force-convert',
    action='store_true',
    help='Force converting to DB.pkl'
)

# query parameter

ARGS.add_argument(
    '-n',
    '--count',
    default=False,
    metavar='COLUMN',
    help='Count the parameter and output list. Just count all, if COLUMN == ALL'
)

ARGS.add_argument(
    '--csv',
    default=False,
    action='store_true',
    help='Handle cell content as CSV'
)

ARGS.add_argument(
    '-l',
    '--list',
    action='store_true',
    help='List possible columns'
)

ARGS.add_argument(
    '-d',
    '--date',
    default='day',
    choices=['year', 'month', 'day'],
    help='Narrow counting to year, month or day'
)

ARGS.add_argument(
    '-s',
    '--sort',
    default='count',
    choices=['value', 'count'],
    help='Sort output by value or count'
)

ARGS.add_argument(
    '-r',
    '--reverse',
    default=False,
    action='store_true',
    help='Sort in reverse'
)

ARGS.add_argument(
    '-f',
    '--filter',
    nargs=2,
    action='append',
    help=(
        'Get filter like [COLUMN] [SEARCH] - also multiple times'
    )
)

ARGS.add_argument(
    '-t',
    '--total',
    default=None,
    metavar='COLUMN',
    help='Try to use the COLUMN value for summing'
)

ARGS = ARGS.parse_args()

if __name__ == '__main__':
    # initialize SETTINGS
    SETTINGS = settings.Settings(
        force_convert=ARGS.force_convert
    )

    # initialize DB
    DB = catalog.Catalog(
        file=ARGS.file,
        settings=SETTINGS
    )

    # instruments count query
    if ARGS.count:
        show, null = DB.count(
            search=ARGS.count,
            csv=ARGS.csv,
            date=ARGS.date,
            sort=ARGS.sort,
            reverse=ARGS.reverse,
            filter=ARGS.filter,
            total=ARGS.total
        )
        if show is False:
            print('Column not found: {}.'.format(ARGS.count))
        else:
            for x in show:
                print('{}: {}'.format(x[0], x[1]))

    # list columns
    if ARGS.list:
        print('Possible columns:')
        print(', '.join(DB.db[0]))
