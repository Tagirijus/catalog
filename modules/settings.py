"""
The settings module.
"""

import os


class Settings(object):
    """Settings object."""

    def __init__(self, force_convert=False):
        """Initialize the class."""
        self.BASE_PATH = os.path.dirname(os.path.realpath(__file__))[
            :os.path.dirname(os.path.realpath(__file__)).rfind('/')
        ]

        # ignore db.pkl file
        self.force_convert = force_convert
