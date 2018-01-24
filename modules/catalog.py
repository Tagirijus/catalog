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

    def count(self, search=None):
        """
        Count and show data.

        Outputs a tuple like this:
            [0] -> sorted list with [0: count], [1: search string]
            [1] -> dict with [search string] = count
        """
        if search not in self.cols.keys():
            return [[0], ['None']], {'None': 0}

        # init ouput dict
        instruments = {}

        # cycle through rows (from first entry, not from title row)
        for row in self.db[1:]:
            index = self.cols[search]

            if index >= len(row):
                continue

            row_instruments_raw = row[index]
            row_instruments = row_instruments_raw.split(', ')

            # cycle through the instruments
            for inst in row_instruments:
                if inst == '':
                    continue
                if inst not in instruments.keys():
                    instruments[inst] = 1
                else:
                    instruments[inst] += 1

        # prepare and sort output
        out = []
        for i in instruments:
            out.append((instruments[i], i))

        out.sort(key=lambda x: x[0], reverse=True)

        # return output
        return out, instruments
