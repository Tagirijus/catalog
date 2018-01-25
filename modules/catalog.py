"""
The catalog module holds the catalog object.

The catalog object can query information.
"""

import datetime
from modules import filecheck


class Catalog(object):
    """The catalog object."""

    def __init__(self, file=None, settings=None):
        """Initialize the class."""
        # get the db
        self.db = filecheck.check(file=file, settings=settings)

        # get cols according to columsn from settings
        self.cols = self.get_cols(settings=settings)

    def get_cols(self, settings=None):
        """Get cols according to columns from settings."""
        # init output cols dict
        cols = {}

        try:
            # cycle through col keys from settings
            for key in settings.columns.keys():
                # search index in first table row (should be the col titles!)
                cols[key] = (
                    self.db[0].index(settings.columns[key])
                )

                # let it be 0 if it's -1
                if cols[key] < 0:
                    cols[key] = 0
                    print('Fetched wrong index for: ' + key)
        except Exception as e:
            print('Could not fetch columns: ' + str(e))

        return cols

    def count(
        self,
        settings=None,
        search=None,
        csv=False,
        date='day',
        sort='count',
        reverse=False,
        filter=None
    ):
        """
        Count and show data.

        Outputs a tuple like this:
            [0] -> sorted list with [0: count], [1: search string]
            [1] -> dict with [search string] = count
        """
        if settings is None:
            print('Catalog.count(): no settings object given.')
            return False, None

        # get the index for the column
        index = self.search_col(
            settings=settings,
            search=search
        )

        if index is False:
            return False, None

        # init output dict
        search_data = {}

        # cycle through rows (from first entry, not from title row - filtered)
        for row in self.filter(settings=settings, filter=filter):
            if index >= len(row):
                continue

            if csv:
                row_search_data_raw = row[index]
                row_search_data = row_search_data_raw.split(', ')
            else:
                row_search_data = [row[index]]

            # cycle through the search_data
            for dat in row_search_data:
                # continue counting, if the cell is empty
                if dat == '':
                    continue

                # alter the dat, if it's a date
                is_date = type(dat).__name__ == 'date'
                is_month = date == 'month'
                is_year = date == 'year'
                if is_date and is_month:
                    dat = '{}-{:02d}'.format(
                        dat.year,
                        dat.month
                    )
                elif is_date and is_year:
                    dat = '{}'.format(
                        dat.year
                    )
                elif is_date:
                    dat = '{}-{:02d}-{:02d}'.format(
                        dat.year,
                        dat.month,
                        dat.day
                    )

                # append the dat to the search_data
                if dat not in search_data.keys():
                    search_data[dat] = 1
                else:
                    search_data[dat] += 1

        # prepare output
        out = []
        for i in search_data:
            out.append((search_data[i], i))

        # sort output by count
        if sort == 'count':
            out.sort(key=lambda x: x[0], reverse=reverse)
        elif sort == 'value':
            out.sort(key=lambda x: x[1], reverse=reverse)

        # return output
        return out, search_data

    def search_col(self, settings=None, search=None):
        """Return internal key of column, if found."""
        # check if the internal column name was given
        internal_col_given = search in self.cols.keys()

        # already output it to prevent searching via for loop
        if internal_col_given:
            return self.cols[search]

        # check if a "translated" column name was given (like form the columns.json)
        translated_col_given = False
        for key, value in settings.columns.items():
            if search == value:
                search = key
                translated_col_given = True
                break

        if not internal_col_given and not translated_col_given:
            return False
        else:
            return self.cols[search]

    def filter(self, settings=None, filter=None):
        """Filter the db."""
        # no filter given
        if type(filter) is not list:
            return self.db[1:]

        # filter given, init out list
        out = self.db[1:]

        # cycle through filters
        for f in filter:
            # continue, if column / f[0] does not exist
            index = self.search_col(
                settings=settings,
                search=f[0]
            )

            if not index:
                print('Could not apply filter. "{}" column not found.'.format(f[0]))
                continue

            # otherwise alter the out list
            # to only include cols including the search term
            tmp = []
            filter_aplied = False
            for row in out:
                # prevent index out of range
                if index >= len(row):
                    continue

                # only append rows, which have the search term in the chosen col
                # check if there is any of these signs on pos 0: >, < or =
                relative_filter = f[1][0] in ['>', '<', '=']

                # get original type of the cell
                cell_type = type(row[index])

                # it's an integer
                if cell_type is int:
                    # can filter be an integer?
                    try:
                        rel_filter_in = int(f[1][1:])
                    except Exception:
                        relative_filter = False

                # it's a date
                if cell_type is datetime.date:
                    # can filter be a date?
                    try:
                        # year-month-day ?
                        rel_filter_in = datetime.datetime.strptime(
                            f[1][1:], '%Y-%m-%d'
                        ).date()
                    except Exception:
                        try:
                            # year-month ?
                            rel_filter_in = datetime.datetime.strptime(
                                f[1][1:], '%Y-%m'
                            ).date()
                        except Exception:
                            try:
                                # year ?
                                rel_filter_in = datetime.datetime.strptime(
                                    f[1][1:], '%Y'
                                ).date()
                            except Exception:
                                relative_filter = False

                # it's a timedelta
                if cell_type is datetime.timedelta:
                    try:
                        # HH:MM:SS or MM:SS ?
                        f_split = [int(i) for i in f[1][1:].split(':')]

                        # HH:MM:SS ?
                        if len(f_split) == 3:
                            rel_filter_in = datetime.timedelta(
                                hours=f_split[0],
                                minutes=f_split[1],
                                seconds=f_split[2],
                            )

                        # MM:SS ?
                        elif len(f_split) == 2:
                            rel_filter_in = datetime.timedelta(
                                minutes=f_split[0],
                                seconds=f_split[1],
                            )

                        # nothing fits really
                        else:
                            relative_filter = False
                    except Exception:
                        relative_filter = False

                # otherwise check according to >, < or =
                if relative_filter:
                    # str: means exclude the given search term
                    if cell_type is str and f[1][0] in ['>', '<']:
                        if str(f[1][1:]) not in str(row[index]):
                            tmp.append(row)
                            filter_aplied = True

                    # str: otherwise it has to be it 100%
                    elif cell_type is str and f[1][0] == '=':
                        if str(f[1][1:]) == str(row[index]):
                            tmp.append(row)
                            filter_aplied = True

                    # int, date, timedelta: cell must be higher int than filter
                    elif cell_type is not str and f[1][0] == '>':
                        if row[index] > rel_filter_in:
                            tmp.append(row)
                            filter_aplied = True

                    # int, date, timedelta: cell must be lower int than filter
                    elif cell_type is not str and f[1][0] == '<':
                        if row[index] < rel_filter_in:
                            tmp.append(row)
                            filter_aplied = True

                    # int, date, timedelta: cell must be equal int than filter
                    elif cell_type is not str and f[1][0] == '=':
                        if row[index] == rel_filter_in:
                            tmp.append(row)
                            filter_aplied = True

                # fallback / non-relative filter
                else:
                    if str(f[1]) in str(row[index]):
                        tmp.append(row)
                        filter_aplied = True

            # the new out list is the tmp with only the found rows
            out = tmp

            # tell the user about the filter application
            if filter_aplied:
                print('Applied filter "{}" for column "{}".'.format(
                    f[1],
                    f[0]
                ))

        return out
