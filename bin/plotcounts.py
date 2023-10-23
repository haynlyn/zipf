"""Brief description of what the script does."""

import argparse
import pandas as pd

def main(args):
    "Run the program."
    df = pd.read_csv(args.infile, header=None,
            names=('word', 'word_frequency'))
    df['rank'] = df['word_frequency'].rank(ascending=False,
                                            method='max')
    ax = df.plot.scatter(x='word_frequency', y='rank',
                         figsize=[12,6], grid=True,
                         loglog=True,
                         xlim=args.xlim)
    ax.figure.savefig(args.outfile)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('infile', type=argparse.FileType('r'), nargs='?',
                        default='-', help='Input file name')
    parser.add_argument('--xlim', default=None, type=float,
                        metavar=('XMIN', 'XMAX'), nargs=2,
                        help='X-axis bounds')
    parser.add_argument('--outfile', default='plotcounts.png', help='Output file name')
    args = parser.parse_args()
    main(args)

