import argparse


def getArguments():
    """Return argparse object."""

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
        help='Handle cell content as CSV with ", " as the seperator in the content'
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
            '"=" only: cell is empty. -f ALL [SEARCH] for filtering in every column, '
            'while "=", ">" and "<" won\'t work then'
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
            '"=" only: cell is empty. -f ALL [SEARCH] for filtering in every column, '
            'while "=", ">" and "<" won\'t work then'
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

    ARGS.add_argument(
        '-e',
        '--empty',
        nargs=2,
        action='append',
        help=(
            'Set how an empty cell for the column will be interpreted while counting. '
            'Value can be string ("abc123"), integer ("0") or date ("1987-10-15")'
        )
    )

    ARGS.add_argument(
        '--unixtimestamp',
        default=False,
        action='store_true',
        help='Convert datetimes / timedeltas to unix timestamp on list output.'
    )

    ARGS.add_argument(
        '--inject',
        nargs=2,
        action='append',
        help=(
            'Use external program commands to manipulate content of a cell like '
            '[COLUMN] [EXECUTABLE]. The program should accept only one string '
            'argument and output a string. The executable string may have a '
            'placeholder which stands for a column. Then during iteration the '
            'command will get the value for the column and the specific row there. '
            'E.g. "TITLE" "echo {NAME}" would replace teh value of the TITLE column '
            'with the value of the NAME column in the same row.'
        )
    )

    return ARGS.parse_args()
