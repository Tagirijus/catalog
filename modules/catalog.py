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
