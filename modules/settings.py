"""
The settings module.

Loads the settings or writes a default settings JSON.
"""

import json
from modules import filecheck
import os

DEFAULT_COLUMNS = {
    'title': 'Title (name)',
    'title id': 'Title (ID)',
    'client id': 'Client (ID)',
    'client company': 'Client (company)',
    'client name': 'Client (name)',
    'project': 'Project',
    'created': 'Created',
    'project file': 'Project file',
    'audio file': 'Audio file',
    'published': 'Published',
    'playing time': 'Playing time',
    'sound alike': 'Sound alike',
    'medium': 'Medium',
    'genre': 'Genre',
    'subgenre': 'Subgenre',
    'bpm': 'BPM',
    'key': 'Key',
    'time signature': 'Time signature',
    'versions': 'Versions',
    'voices count composition': 'Voices count (composition)',
    'voices composition': 'Voices (composition)',
    'ensemble': 'Ensemble',
    'voices count recording': 'Voices count (recording)',
    'voices recording': 'Voices (recording)',
    'musicians count': 'Musicians count',
    'musicians names': 'Musicians (names)',
    'notes': 'Notes',
    'composition': 'Composition',
    'arrangement': 'Arrangement',
    'idea': 'Idea',
    'script text': 'Script / text',
    'voice actors count': 'Voice actors count',
    'voice actors names': 'Voice actors (names)',
    'licensing agency history': 'Licensing agency (history)',
    'licensing agency actual': 'Licensing agency (actual)',
    'license type': 'License type',
    'non exclusive right': 'Non-exclusive right',
    'exclusive right': 'Exclusive right',
    'working time': 'Working time',
    'income project': 'Income (project)',
    'income license': 'Income (license)',
    'income total': 'Income (total)',
    'rating': 'Rating',
    'tags': 'Tags',
    'tags foreign': 'Tags (foreign)',
    'description': 'Description',
    'description foreign': 'Description (foreign)'
}


class Settings(object):
    """Settings object."""

    def __init__(self, columns_file=None, force_convert=False):
        """Initialize the class."""
        self.BASE_PATH = os.path.dirname(os.path.realpath(__file__))[
            :os.path.dirname(os.path.realpath(__file__)).rfind('/')
        ]

        # ignore db.pkl file
        self.force_convert = force_convert

        # init default columns
        self.columns = DEFAULT_COLUMNS

        # try to load the columns from given file
        try:
            with open(columns_file, 'r') as f:
                self.columns = json.loads(f.read())
        except Exception:
            print('Could not load columns file.')

    def dump_default_columns_to_file(self, file=None):
        """Dump defualt values to file."""
        if filecheck.exists(file):
            print('File already exists.')
        else:
            with open(file, 'w') as f:
                f.write(json.dumps(DEFAULT_COLUMNS, indent=2))
            print('Default columns written to: ' + str(file))
