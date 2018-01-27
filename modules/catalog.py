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

        # get cols according to columsn from file
        self.cols = self.get_cols()

    def get_cols(self):
        """Get cols according to columns from file."""
        # init output cols dict
        cols = {}

        # get cols and their index
        for i, x in enumerate(self.db[0]):
            cols[x] = i

        return cols

    def count(
        self,
        search=None,
        csv=False,
        date='day',
        sort='count',
        reverse=False,
        filter=None,
        filter_or=None,
        total=None,
        quiet=False
    ):
        """
        Count and show data.

        Outputs a tuple like this:
            [0] -> sorted list with [0: count], [1: search string]
            [1] -> dict with [search string] = count
        """
        # get the index for the column
        index = self.search_col(search=search)

        if index is False and search != 'ALL':
            return False, None
        elif search == 'ALL':
            index = 0
            # csv disabled prevents listing more rows than there are
            csv = False

        # init output dict
        search_data = {}

        rows = self.get_filtered_rows(
            filter=filter,
            filter_or=filter_or,
            quiet=quiet
        )

        for row in rows:
            if index >= len(row):
                continue

            if csv and type(row[index]) is str:
                row_search_data_raw = row[index]
                row_search_data = row_search_data_raw.split(', ')
            else:
                row_search_data = [row[index]]

            # cycle through the search_data
            for i, dat in enumerate(row_search_data):
                # continue counting, if the cell is empty and search != 'ALL'
                if dat == '' and search != 'ALL':
                    continue

                # alter the dat, if it's a date
                is_date = type(dat) is datetime.date
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

                # check if total COLUMN exists
                total_column = self.search_col(search=total)

                # simply use integer as counting as fallback
                add_me = 1

                # get value to add
                if total_column is not False:
                    # skip, if index out of range
                    if total_column >= len(row):
                        continue

                    # also continue, if cell is empty
                    if row[total_column] == '':
                        continue

                    # check if type can be summed up
                    row_type = type(row[total_column])

                    # ready to be summed: int, timedelta, float
                    if (
                        row_type is int or
                        row_type is datetime.timedelta or
                        row_type is float
                    ):
                        add_me = row[total_column]

                # count all rows, if search == 'ALL'
                if search == 'ALL':
                    dat = 'All'

                # append the dat to the search_data
                if dat not in search_data.keys():
                    # and begin wih simple counting
                    search_data[dat] = add_me

                # try to append it, but check if type is correct
                else:
                    try:
                        search_data[dat] += add_me
                    except Exception:
                        print('Could not add:', row[index])

        # prepare output
        out = []
        for i in search_data:
            # round count, if it's a float
            if type(search_data[i]) is float:
                search_data[i] = round(search_data[i])

            # append it to the out variable
            out.append((search_data[i], i))

        # sort output by count
        if sort == 'value':
            out.sort(key=lambda x: x[0], reverse=reverse)
        else:
            try:
                out.sort(key=lambda x: x[1], reverse=reverse)
            except Exception:
                if not quiet:
                    print('Cannot sort. Different count types?')

        # return output
        return out, search_data

    def search_col(self, search=None):
        """Return index of column, if found."""
        if search in self.cols:
            return self.cols[search]
        else:
            return False

    def filter(self, input_list=None, filter=None, indexes_found=None, quiet=False):
        """Filter the db and output all applyable indexes as a list."""
        # no filter given
        if type(filter) is not list:
            return [input_list.index(x) for x in input_list]

        # indexes_found are all indexes, if no list is given
        if indexes_found is None:
            indexes_found = [input_list.index(x) for x in input_list]

        # filter given, init out list
        out = []

        # continue, if column / filter[0] does not exist
        index = self.search_col(search=filter[0])

        if index is False and not quiet:
            print('Could not apply filter. "{}" column not found.'.format(filter[0]))
            return [input_list.index(x) for x in input_list]

        # otherwise get only rows, which fits the filter needs
        filter_aplied = False
        for row_index, row in enumerate(input_list):
            # prevent index out of range
            if index >= len(row):
                continue

            # only append rows, which have the search term in the chosen col
            # check if there is any of these signs on pos 0: >, <, = or #
            relative_filter = filter[1][0] in ['>', '<', '=', '#']

            # get original type of the cell
            cell_type = type(row[index])

            # it's an integer
            if cell_type is int:
                # can filter be an integer?
                try:
                    rel_filter_in = int(filter[1][1:])
                except Exception:
                    relative_filter = False

            # it's a date
            if cell_type is datetime.date:
                # can filter be a date?
                date_full = False
                date_year_month = False
                date_year = False
                try:
                    # year-month-day ?
                    rel_filter_in = datetime.datetime.strptime(
                        filter[1][1:], '%Y-%m-%d'
                    ).date()
                    date_full = True
                except Exception:
                    try:
                        # year-month ?
                        rel_filter_in = datetime.datetime.strptime(
                            filter[1][1:], '%Y-%m'
                        ).date()
                        date_year_month = True
                    except Exception:
                        try:
                            # year ?
                            rel_filter_in = datetime.datetime.strptime(
                                filter[1][1:], '%Y'
                            ).date()
                            date_year = True
                        except Exception:
                            relative_filter = False

            # it's a timedelta
            if cell_type is datetime.timedelta:
                try:
                    # HH:MM:SS or MM:SS ?
                    f_split = [int(i) for i in filter[1][1:].split(':')]

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

            # otherwise check according to >, <, = or #
            if relative_filter:
                # get checking variables
                cell_is_str = cell_type is str
                cell_is_int_or_time = (
                    cell_type is int or
                    cell_type is datetime.timedelta
                )
                cell_is_date_full = (
                    cell_type is datetime.date and
                    date_full
                )
                cell_is_date_year_month = (
                    cell_type is datetime.date and
                    date_year_month
                )
                cell_is_date_year = (
                    cell_type is datetime.date and
                    date_year
                )

                # str: means exclude the given search term
                if cell_is_str and filter[1][0] in ['>', '<', '#']:
                    if str(filter[1][1:]) not in str(row[index]):
                        out += [row_index] if row_index in indexes_found else []
                        filter_aplied = True

                # str: otherwise it has to be it 100%
                elif cell_is_str and filter[1][0] == '=':
                    if str(filter[1][1:]) == str(row[index]):
                        out += [row_index] if row_index in indexes_found else []
                        filter_aplied = True

                # int, timedelta: cell must be higher int than filter
                elif cell_is_int_or_time and filter[1][0] == '>':
                    if row[index] > rel_filter_in:
                        out += [row_index] if row_index in indexes_found else []
                        filter_aplied = True

                # int, timedelta: cell must be lower int than filter
                elif cell_is_int_or_time and filter[1][0] == '<':
                    if row[index] < rel_filter_in:
                        out += [row_index] if row_index in indexes_found else []
                        filter_aplied = True

                # int, timedelta: cell must be equal int than filter
                elif cell_is_int_or_time and filter[1][0] == '=':
                    if row[index] == rel_filter_in:
                        out += [row_index] if row_index in indexes_found else []
                        filter_aplied = True

                # int, timedelta: cell must not be equal int than filter
                elif cell_is_int_or_time and filter[1][0] == '#':
                    if row[index] != rel_filter_in:
                        out += [row_index] if row_index in indexes_found else []
                        filter_aplied = True

                # date (full): cell must be higher date (full) than filter
                elif cell_is_date_full and filter[1][0] == '>':
                    if row[index] > rel_filter_in:
                        out += [row_index] if row_index in indexes_found else []
                        filter_aplied = True

                # date (full): cell must be lower date (full) than filter
                elif cell_is_date_full and filter[1][0] == '<':
                    if row[index] < rel_filter_in:
                        out += [row_index] if row_index in indexes_found else []
                        filter_aplied = True

                # date (full): cell must be equal date (full) than filter
                elif cell_is_date_full and filter[1][0] == '=':
                    if row[index] == rel_filter_in:
                        out += [row_index] if row_index in indexes_found else []
                        filter_aplied = True

                # date (full): cell must not be equal date (full) than filter
                elif cell_is_date_full and filter[1][0] == '#':
                    if row[index] != rel_filter_in:
                        out += [row_index] if row_index in indexes_found else []
                        filter_aplied = True

                # date (Y-m): cell must be higher date (Y-m) than filter
                elif cell_is_date_year_month and filter[1][0] == '>':
                    if (
                        row[index].strftime('%Y-%m') >
                        rel_filter_in.strftime('%Y-%m')
                    ):
                        out += [row_index] if row_index in indexes_found else []
                        filter_aplied = True

                # date (Y-m): cell must be lower date (Y-m) than filter
                elif cell_is_date_year_month and filter[1][0] == '<':
                    if (
                        row[index].strftime('%Y-%m') <
                        rel_filter_in.strftime('%Y-%m')
                    ):
                        out += [row_index] if row_index in indexes_found else []
                        filter_aplied = True

                # date (Y-m): cell must be equal date (Y-m) than filter
                elif cell_is_date_year_month and filter[1][0] == '=':
                    if (
                        row[index].strftime('%Y-%m') ==
                        rel_filter_in.strftime('%Y-%m')
                    ):
                        out += [row_index] if row_index in indexes_found else []
                        filter_aplied = True

                # date (Y-m): cell must not be equal date (Y-m) than filter
                elif cell_is_date_year_month and filter[1][0] == '#':
                    if (
                        row[index].strftime('%Y-%m') !=
                        rel_filter_in.strftime('%Y-%m')
                    ):
                        out += [row_index] if row_index in indexes_found else []
                        filter_aplied = True

                # date (year): cell must be higher date (year) than filter
                elif cell_is_date_year and filter[1][0] == '>':
                    if row[index].year > rel_filter_in.year:
                        out += [row_index] if row_index in indexes_found else []
                        filter_aplied = True

                # date (year): cell must be lower date (year) than filter
                elif cell_is_date_year and filter[1][0] == '<':
                    if row[index].year < rel_filter_in.year:
                        out += [row_index] if row_index in indexes_found else []
                        filter_aplied = True

                # date (year): cell must be equal date (year) than filter
                elif cell_is_date_year and filter[1][0] == '=':
                    if row[index].year == rel_filter_in.year:
                        out += [row_index] if row_index in indexes_found else []
                        filter_aplied = True

                # date (year): cell must not be equal date (year) than filter
                elif cell_is_date_year and filter[1][0] == '#':
                    if row[index].year != rel_filter_in.year:
                        out += [row_index] if row_index in indexes_found else []
                        filter_aplied = True

            # fallback / non-relative filter
            else:
                if str(filter[1]) in str(row[index]):
                    out += [row_index] if row_index in indexes_found else []
                    filter_aplied = True

        # tell the user about the filter application
        if filter_aplied and not quiet:
            print('Applied filter "{}" for column "{}".'.format(
                filter[1],
                filter[0]
            ))

        return out

    def get_filtered_rows(self, filter=None, filter_or=None, quiet=False):
        """Return the filtered row list."""
        # filter the list (excluding)
        if type(filter) is list:
            # init filtered list (get all indexes as well in list)
            rows_filtered = []
            indexes_found = self.filter(input_list=self.db[1:], quiet=quiet)

            # append found row indexes
            for f in filter:
                rows_filtered = self.filter(
                    input_list=self.db[1:],
                    filter=f,
                    indexes_found=indexes_found,
                    quiet=quiet
                )

                # refresh indexes_found to new found indexes
                indexes_found = rows_filtered
        else:
            rows_filtered = []

        # filter the list (including)
        if type(filter_or) is list:
            # init filtered_or list (no indexes at start)
            rows_filtered_or = []

            # append found row indexes
            for fo in filter_or:
                rows_filtered_or += self.filter(
                    input_list=self.db[1:],
                    filter=fo,
                    quiet=quiet
                )
        else:
            rows_filtered_or = []

        # no filter given at all, use the whole list then
        if type(filter) is not list and type(filter_or) is not list:
            return self.db[1:]

        # filter given, combine their row indexes
        else:
            rows_indexes = rows_filtered + rows_filtered_or

        # now get only the rows with the indexes in rows_indexes
        return [x for x in self.db[1:] if self.db[1:].index(x) in rows_indexes]

    def list(
        self,
        sort=False,
        reverse=False,
        filter=None,
        filter_or=None,
        header=False,
        quiet=True
    ):
        """List all rows."""
        if header:
            rows = [self.db[0]]
        else:
            rows = []

        rows += self.get_filtered_rows(
            filter=filter,
            filter_or=filter_or,
            quiet=quiet
        )

        # do the sorting stuff
        sorting_column = self.search_col(search=sort)

        if sorting_column is not False:
            rows.sort(key=lambda x: x[sorting_column], reverse=reverse)

        # output the rows
        return rows
