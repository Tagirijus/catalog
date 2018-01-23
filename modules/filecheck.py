"""
This module checks certain file specific things.

It checks if the given file exists. It also checks if the ODS is newer
than the converted CSV file and converts it then. The mechanic is for
lowering the loading time of the programm, if the original ODS did not
change. For a big ODS the programm would start slowly otherwise.
"""

import csv
import os
from pyexcel_ods import get_data

path_to_module = os.path.dirname(os.path.realpath(__file__))
DB_FILE = path_to_module + '/db.csv'


def check(file=None):
    """Check file and return list."""

    # no file parameter given
    file_given = file is not None

    # file given, but not valid - exit programm immediately
    if file_given and not os.path.isfile(file):
        print('No valid file given.')
        exit()

    # DB_FILE already exists?
    db_exists = os.path.isfile(DB_FILE)

    # no file given at all, use DB_FILE instead
    if not file_given and db_exists:
        return load_db(DB_FILE)

    # file given, no DB_FILE, convert it, then output it
    elif file_given and not db_exists:
        convert(file)
        return load_db(DB_FILE)

    # file given, DB_FILE exists, check which is newer, convert, then output
    elif file_given and db_exists:
        # get dates
        file_mod_date = os.path.getmtime(file)
        db_mod_date = os.path.getmtime(DB_FILE)

        # convert if file is newer
        if file_mod_date > db_mod_date:
            convert(file)

        # output db
        return load_db(DB_FILE)

    # something else happens
    else:
        print('I am not sure, what happened ... woops.')
        exit()


def load_db(file=None):
    """Load the CSV and return a list."""
    if file is not None:
        db = []
        with open(file, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                db.append(row)
        return db
    else:
        print('Error while loading the CSV.')
        return []


def convert(file=None):
    """Convert given ODS to DB_FILE."""
    try:
        # get the data from the ODS
        data = get_data(file)

        # get the first table only
        for i, x in enumerate(data.keys()):
            if i == 0:
                table = data[x]
                break

        # save this table in the DB_FILE
        with open(DB_FILE, 'w') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
            for row in table:
                spamwriter.writerow(row)
    except Exception as e:
        raise e
