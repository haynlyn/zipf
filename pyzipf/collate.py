"""
Combine multiple word count CSV-files
into a single cumulative count.
"""

import csv
import argparse
from collections import Counter

import pyzipf.utilities as util

import logging


def update_counts(reader, word_counts):
    """Update word coutns with data from another reader/file."""
    for word, count in csv.reader(reader):
        word_counts[word] += int(count)


def process_file(fname, word_counts):
    """Read file and update word counts"""
    logging.debug(f'Reading in {fname}...')
    if not fname.endswith('.csv'):
        msg = util.ERRORS['not_csv_suffix'].format(fname=fname)
        raise OSError(msg)
    with open(fname, 'r') as reader:
        logging.debug('Computing word counts...')
        update_counts(reader, word_counts)
    

def main(args):
    """Run the command line program."""
    word_counts = Counter()
    logging.info('Processing files...')
    for fname in args.infiles:
        try:
            process_file(fname, word_counts)
        except FileNotFoundError:
            msg = util.ERRORS['file_not_found'].format(fname=fname)
            logging.warning(FileNotFoundError(msg))
        except PermissionError:
            msg = util.ERRORS['permissions_problem'].format(fname=fname)
            logging.warning(PermissionError(msg))
        except Exception as e:
            msg = f'{fname} not processed: {e}'
            logging.error(Exception(msg))
    util.collection_to_csv(word_counts, num=args.num)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('infiles', type=str, nargs='*', help='Input file names')
    parser.add_argument('-n', '--num', type=int, default=None, help='Output n most frequent words')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='If true, changes logging from `WARNING` to `DEBUG`')
    parser.add_argument('-l', '--logfile', type=str, default='collate.log',
                        help='File to which to write logs')
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, filename=args.logfile, filemode='w')
    main(args)

