"""
Programm for analyzing an ODS spreadsheet.

The program takes a file as argument (ODS file) and loads its columns
and rows into the database. Then you can filter and search things.
"""

from modules import arguments
from modules import catalog
from modules import settings

ARGS = arguments.getArguments()

if __name__ == '__main__':
    # initialize SETTINGS
    SETTINGS = settings.Settings(
        force_convert=ARGS.force_convert
    )

    # initialize DB
    DB = catalog.Catalog(
        file=ARGS.file,
        settings=SETTINGS,
        quiet=ARGS.quiet,
        inject=ARGS.inject
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
            all=ARGS.all,
            empty=ARGS.empty
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
            ignore_case=ARGS.ignore_case,
            empty=ARGS.empty,
            unixtimestamp=ARGS.unixtimestamp
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
