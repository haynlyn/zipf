"""
Count the occurrences of all sentence endings (".", "?", "!") in a text.
"""

import argparse
import string
from collections import defaultdict

#import utilities as util


def count_punct(reader):
    """Count the occurrence of each punctuation in a string."""
    count_dict = defaultdict(int)
    text = reader.read()
    puncts = ['.', '?', '!']
    for p in puncts:
        count_dict[p] += text.count(p)
        print("Number of {} is {}".format(p, count_dict[p]))


def main(args):
    """Run the command line program."""
    punct_counts = count_punct(args.infile)
    #util.collection_to_csv(word_counts, num=args.num)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('infile', type=argparse.FileType('r'),
                        nargs='?', default='-', help='Input file name')
    #parser.add_argument('-n', '--num', type=int, default=None, help='Output n most frequent words')
    args = parser.parse_args()
    main(args)

