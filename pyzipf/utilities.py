"""Collection of commonly used functions."""

import sys
import csv

def collection_to_csv(collection, num=None):
    """
    Write out collection of items and counts in csv format.

    Parameters
    ----------
    collection : collections.Counter
        Collection of items and counts
    num : int
        Limit output to N most frequent items
    """
    collection = collection.most_common()
    
    if num is None:
        num = len(collection)
    writer = csv.writer(sys.stdout)
    writer.writerows(collection[:num])

ERRORS = {
    'not_csv_suffix' : '{fname}: File must end in .csv',
    'config_corrupted': '{config_name} corrupted',
    'file_not_found' : '{fname}: File not found',
    'permissions_problem' : 'Problem with permissions'
}
