"""
The catalog module holds the catalog object.

The catalog object can query information.
"""

from modules import filecheck


class Catalog(object):
    """The catalog object."""

    def __init__(self, file=None):
        """Initialize the class."""
        self.db = filecheck.check(file=file)
