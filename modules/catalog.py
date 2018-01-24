"""
The catalog module holds the catalog object.

The catalog object can query information.
"""

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
        reverse=False
    ):
        """
        Count and show data.

        Outputs a tuple like this:
            [0] -> sorted list with [0: count], [1: search string]
            [1] -> dict with [search string] = count
        """
        if settings is None:
            return False, None

        # check if the internal column name was given
        internal_col_given = search in self.cols.keys()

        # check if a "translated" column name was given (like form the columns.json)
        translated_col_given = False
        for key, value in settings.columns.items():
            if search == value:
                search = key
                translated_col_given = True

        if not internal_col_given and not translated_col_given:
            return False, None

        # init output dict
        search_data = {}

        # cycle through rows (from first entry, not from title row)
        for row in self.db[1:]:
            index = self.cols[search]

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
