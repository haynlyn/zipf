"""Brief description of what the script does."""

import argparse
import pandas as pd

def main(args):
    "Run the program."
    print('Input file:', args.infile)
    print('Output file:', args.outfile)
    input_csv, output_img = args.infile, args.outfile

    df = pd.read_csv(input_csv, header=None,
            names=('word', 'word_frequency'))
    df['rank'] = df['word_frequency'].rank(ascending=False,
                                            method='max')
    df['inverse_rank'] = 1/df['rank']
    if args.xlim is not None:
        xbounds = args.xlim
        xbounds = (int(x) for x in xbounds.split(','))
        scatplot = df.plot.scatter(x='word_frequency', y='inverse_rank',
                               figsize=[12, 6], grid=True,
                                xlim=xbounds)
    else:
        scatplot = df.plot.scatter(x='word_frequency', y='inverse_rank',
                            figsize=[12, 6], grid=True)

    fig = scatplot.get_figure()
    fig.savefig(output_img)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('infile', type=argparse.FileType('r'), nargs='?',
                        default='-', help='Input file name')
    parser.add_argument('--xlim', default=None, type=str, nargs='?',
                        help='X-axis bounds')
    parser.add_argument('--outfile', default='plotcounts.png', help='Output file name')
    args = parser.parse_args()
    main(args)

