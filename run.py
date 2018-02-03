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
    '-c',
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
    '--columns',
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
    metavar='{value,count} / COLUMN',
    help='Sort output by "value" or "count" or any column, if used with the -l argument.'
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
        'Get excluding filter(s) like [COLUMN] [SEARCH]. '
        '<: lower, >: higher, =: equal, #: unequal, '
        '"#" only: cell is not empty and '
        '"=" only: cell is empty'
    )
)

ARGS.add_argument(
    '-o',
    '--filter-or',
    nargs=2,
    action='append',
    help=(
        'Get including filter(s) like [COLUMN] [SEARCH] '
        '<: lower, >: higher, =: equal, #: unequal, '
        '"#" only: cell is not empty and '
        '"=" only: cell is empty'
    )
)

ARGS.add_argument(
    '-t',
    '--total',
    default=None,
    metavar='COLUMN',
    help='Try to use the COLUMN value for summing'
)

ARGS.add_argument(
    '-l',
    '--list',
    action='store_true',
    help='List rows of the table'
)

ARGS.add_argument(
    '--header',
    default=False,
    action='store_true',
    help='Enable header while listing rows of the table'
)

ARGS.add_argument(
    '--seperator',
    default=',',
    help='The seperator for the columns while listing rows of the table'
)

ARGS.add_argument(
    '-q',
    '--quiet',
    default=False,
    action='store_true',
    help=(
        'Makes output quiet - except for the table. '
        'Good for CSV format output direct to file via "run.py [arguments] > file.csv'
    )
)

ARGS.add_argument(
    '-a',
    '--append',
    action='append',
    metavar='COLUMN',
    help=(
        'Append a column in list output. Multiple usage of this argument is possible. '
        'Append has higher priortiy than block'
    )
)

ARGS.add_argument(
    '-b',
    '--block',
    action='append',
    metavar='COLUMN',
    help=(
        'Block a column in list output. Multiple usage of this argument is possible. '
        'Block has lower priortiy than append'
    )
)

ARGS.add_argument(
    '-i',
    '--ignore-case',
    default=False,
    action='store_true',
    help='Ignores the case sensitivity for all given strings from the user'
)

ARGS.add_argument(
    '--all',
    default=False,
    action='store_true',
    help='Also count total of searched items and store it as "TOTAL"'
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
        settings=SETTINGS,
        quiet=ARGS.quiet
    )

    # count query
    if ARGS.count:
        show, null = DB.count(
            search=ARGS.count,
            csv=ARGS.csv,
            date=ARGS.date,
            sort=ARGS.sort,
            reverse=ARGS.reverse,
            filter=ARGS.filter,
            filter_or=ARGS.filter_or,
            total=ARGS.total,
            quiet=ARGS.quiet,
            ignore_case=ARGS.ignore_case,
            all=ARGS.all
        )
        if show is False:
            print('Column not found: {}.'.format(ARGS.count))
        else:
            for x in show:
                print('{}: {}'.format(x[0], x[1]))

    # show all rows
    if ARGS.list:
        show = DB.list(
            sort=ARGS.sort,
            reverse=ARGS.reverse,
            filter=ARGS.filter,
            filter_or=ARGS.filter_or,
            header=ARGS.header,
            quiet=ARGS.quiet,
            append=ARGS.append,
            block=ARGS.block,
            ignore_case=ARGS.ignore_case
        )
        for row in show:
            this_row = []
            for col in row:
                try:
                    this_row += [
                        '"{}"'.format(col)
                        if ARGS.seperator in col
                        else col
                    ]
                except Exception:
                    this_row += [str(col)]
            print(ARGS.seperator.join(this_row))

    # list columns
    if ARGS.columns:
        if not ARGS.quiet:
            print('Possible columns:')
        print(ARGS.seperator.join([str(col) for col in DB.db[0]]))
