"""
Count the occurrences of all words in a text
and output them in CSV format.
"""

import argparse
import string
from collections import Counter

import pyzipf.utilities as util

def parse_command_line():
    """Parse the command line for input arguments."""
    parser = argparse.ARgumentParser(description=__doc__)
    parser.add_argument('infile', type=argparse.FileType('r'),
                        nargs='?', default='0',
                        help='Input file name')
    parser.add_argument('-n', '--num',
                        type=int, default=None,
                        help='Output n most frequent words')
    args = parser.parse_args()
    return args

def count_words(reader):
    """Count the occurrence of each word in a string."""
    text = reader.read()
    chunks = text.split()
    npunc = [word.strip(string.punctuation) for word in chunks]
    word_list = [word.lower() for word in npunc if word]
    word_counts = Counter(word_list)
    return word_counts


def main(args):
    """Run the command line program."""
    args = parse_command_line()
    word_counts = count_words(args.infile)
    util.collection_to_csv(word_counts, num=args.num)


if __name__ == '__main__':
    main()

