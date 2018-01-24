"""
The settings module.

Loads the settings or writes a default settings JSON.
"""

import json
from modules import filecheck
import os


DEFAULT_COLUMNS = {
    'title': {
        'caption': 'Title (name)',
        'contains csv': False
    },
    'title id': {
        'caption': 'Title (ID)',
        'contains csv': False
    },
    'client id': {
        'caption': 'Client (ID)',
        'contains csv': False
    },
    'client company': {
        'caption': 'Client (company)',
        'contains csv': False
    },
    'client name': {
        'caption': 'Client (name)',
        'contains csv': False
    },
    'project': {
        'caption': 'Project',
        'contains csv': False
    },
    'created': {
        'caption': 'Created',
        'contains csv': False
    },
    'project file': {
        'caption': 'Project file',
        'contains csv': False
    },
    'audio file': {
        'caption': 'Audio file',
        'contains csv': False
    },
    'published': {
        'caption': 'Published',
        'contains csv': False
    },
    'playing time': {
        'caption': 'Playing time',
        'contains csv': False
    },
    'sound alike': {
        'caption': 'Sound alike',
        'contains csv': True
    },
    'medium': {
        'caption': 'Medium',
        'contains csv': False
    },
    'genre': {
        'caption': 'Genre',
        'contains csv': False
    },
    'subgenre': {
        'caption': 'Subgenre',
        'contains csv': False
    },
    'bpm': {
        'caption': 'BPM',
        'contains csv': False
    },
    'key': {
        'caption': 'Key',
        'contains csv': False
    },
    'time signature': {
        'caption': 'Time signature',
        'contains csv': False
    },
    'versions': {
        'caption': 'Versions',
        'contains csv': True
    },
    'voices count composition': {
        'caption': 'Voices count (composition)',
        'contains csv': False
    },
    'voices composition': {
        'caption': 'Voices (composition)',
        'contains csv': True
    },
    'ensemble': {
        'caption': 'Ensemble',
        'contains csv': False
    },
    'voices count recording': {
        'caption': 'Voices count (recording)',
        'contains csv': False
    },
    'voices recording': {
        'caption': 'Voices (recording)',
        'contains csv': True
    },
    'musicians count': {
        'caption': 'Musicians count',
        'contains csv': False
    },
    'musicians names': {
        'caption': 'Musicians (names)',
        'contains csv': True
    },
    'notes': {
        'caption': 'Notes',
        'contains csv': False
    },
    'composition': {
        'caption': 'Composition',
        'contains csv': False
    },
    'arrangement': {
        'caption': 'Arrangement',
        'contains csv': False
    },
    'idea': {
        'caption': 'Idea',
        'contains csv': True
    },
    'script text': {
        'caption': 'Script / text',
        'contains csv': True
    },
    'voice actors count': {
        'caption': 'Voice actors count',
        'contains csv': False
    },
    'voice actors names': {
        'caption': 'Voice actors (names)',
        'contains csv': True
    },
    'licensing agency history': {
        'caption': 'Licensing agency (history)',
        'contains csv': True
    },
    'licensing agency actual': {
        'caption': 'Licensing agency (actual)',
        'contains csv': True
    },
    'license type': {
        'caption': 'License type',
        'contains csv': False
    },
    'non exclusive right': {
        'caption': 'Non-exclusive right',
        'contains csv': False
    },
    'exclusive right': {
        'caption': 'Exclusive right',
        'contains csv': False
    },
    'working time': {
        'caption': 'Working time',
        'contains csv': False
    },
    'income project': {
        'caption': 'Income (project)',
        'contains csv': False
    },
    'income license': {
        'caption': 'Income (license)',
        'contains csv': False
    },
    'income total': {
        'caption': 'Income (total)',
        'contains csv': False
    },
    'rating': {
        'caption': 'Rating',
        'contains csv': False
    },
    'tags': {
        'caption': 'Tags',
        'contains csv': True
    },
    'tags foreign': {
        'caption': 'Tags (foreign)',
        'contains csv': True
    },
    'description': {
        'caption': 'Description',
        'contains csv': False
    },
    'description foreign': {
        'caption': 'Description (foreign)',
        'contains csv': False
    }
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
