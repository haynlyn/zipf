"""
List the files in a given directory with a given suffix.
"""

import glob
import argparse
from os.path import join

def main(args):
    directory, suffix = args.dir, args.suffix
    psuffix = '*' + suffix
    results = glob.glob(join(directory, psuffix))
    results.sort()
    print(results)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dir', type=str, help='Directory')
    parser.add_argument('suffix', type=str, help='File suffix (e.g. py, sh)')
    args = parser.parse_args()
    main(args)

