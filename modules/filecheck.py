"""
This module checks certain file specific things.

It checks if the given file exists. It also checks if the ODS is newer
than the converted PKL file and converts it then. The mechanic is for
lowering the loading time of the programm, if the original ODS did not
change. For a big ODS the programm would start slowly otherwise.
"""

import datetime
import os
import pickle
from pyexcel_ods import get_data


def check(file=None, settings=None):
    """Check file and return list."""
    # try to create DB_FILE absolute path
    try:
        DB_FILE = settings.BASE_PATH + '/DB.pkl'
    except Exception:
        DB_FILE = os.path.dirname(os.path.realpath(__file__)) + '/DB.pkl'

    # no file parameter given
    file_given = file is not None

    # file given, but not valid - exit programm immediately
    if file_given and not exists(file):
        print('No valid file given.')
        exit()

    # DB_FILE already exists?
    try:
        db_exists = exists(DB_FILE) and not settings.force_convert
    except Exception:
        print('Error with settings object.')
        exit()

    # no file given at all, use DB_FILE instead
    if not file_given and db_exists:
        return load_db(DB_FILE)

    # file given, no DB_FILE, convert it, then output it
    elif file_given and not db_exists:
        convert(file, DB_FILE)
        return load_db(DB_FILE)

    # file given, DB_FILE exists, check which is newer, convert, then output
    elif file_given and db_exists:
        # get dates
        file_mod_date = os.path.getmtime(file)
        db_mod_date = os.path.getmtime(DB_FILE)

        # convert if file is newer
        if file_mod_date > db_mod_date:
            convert(file, DB_FILE)

        # output db
        return load_db(DB_FILE)

    # something else happens
    else:
        print('I am not sure, what happened ... woops.')
        exit()


def load_db(file=None):
    """Load the CSV and return a list."""
    db = []
    if file is not None:
        with open(file, 'rb') as load:
            db = pickle.load(load)
    else:
        print('Error while loading the PKL.')
    return db


def convert(file=None, db_file=None):
    """Convert given ODS to DB_FILE."""
    try:
        # get the data from the ODS
        data = get_data(file)

        # get the first table only and save it to PKL
        for i, x in enumerate(data.keys()):
            if i == 0:
                # get the temp table
                table = []

                # convert every datetime.time to datetime.timedelta
                for row in data[x]:
                    table.append(
                        [convert_to_timedelta(time=y) for y in row]
                    )

                # write it to PKL
                with open(db_file, 'wb') as output:
                    pickle.dump(table, output)
                for debug in table:
                    print(debug)
                print('Converted {} to {}'.format(
                    file,
                    db_file
                ))
                break
    except Exception as e:
        raise e


def convert_to_timedelta(time=None):
    """Convert time to timedelta."""
    if type(time) is datetime.time:
        return datetime.datetime.combine(
            datetime.date.min, time
        ) - datetime.datetime.min
    else:
        return time


def exists(file=None):
    """Check if file exists."""
    return os.path.isfile(file)
