"""Plot word counts."""

import argparse

import yaml
import numpy as np
import pandas as pd
import matplotlib as mpl
from scipy.optimize import minimize_scalar

mpl_plot_styles=['Solarize_Light2',
    '_classic_test_patch',
    '_mpl-gallery',
    '_mpl-gallery-nogrid',
    'bmh',
    'classic',
    'dark_background',
    'fast',
    'fivethirtyeight',
    'ggplot',
    'grayscale',
    'seaborn-v0_8',
    'seaborn-v0_8-bright',
    'seaborn-v0_8-colorblind',
    'seaborn-v0_8-dark',
    'seaborn-v0_8-dark-palette',
    'seaborn-v0_8-darkgrid',
    'seaborn-v0_8-deep',
    'seaborn-v0_8-muted',
    'seaborn-v0_8-notebook',
    'seaborn-v0_8-paper',
    'seaborn-v0_8-pastel',
    'seaborn-v0_8-poster',
    'seaborn-v0_8-talk',
    'seaborn-v0_8-ticks',
    'seaborn-v0_8-white',
    'seaborn-v0_8-whitegrid',
    'tableau-colorblind10']



def nlog_likelihood(beta, counts):
    """Log-likelihood function."""
    likelihood = -np.sum(np.log((1/counts)**(beta - 1)
                                - (1/(counts + 1))**(beta - 1)))
    return likelihood


def get_power_law_params(word_counts):
    """Get the power law parameters.

    References
    ----------
    Moreno-Sanchez et al (2016) define alpha (Eq. 1),
        beta (Eq. 2) and the maximum likelihood estimation (mle)
        of beta (Eq. 6).

    Moreno-Sanchez I, Font-Clos F, Corral A (2016)
        Large-Scale Analysis of Zipf's Law in English Texts.
        PLoS ONE 11(1): e0147073.
        https://doi.org/10.1371/journal.pone/0147073
    """
    mle = minimize_scalar(nlog_likelihood,
                          bracket=(1 + 1e-10, 4),
                          args=word_counts,
                          method='brent')
    beta = mle.x
    alpha = 1/(beta - 1)
    return alpha


def set_plot_params(param_file):
    """Set the matplotlib parameters."""
    if param_file:
        with open(param_file, 'r') as reader:
            param_dict = yaml.load(reader,
                                   Loader=yaml.BaseLoader)
    else:
        param_dict = {}
    for param, value in param_dict.items():
        mpl.rcParams[param] = value

def plot_fit(curve_xmin, curve_xmax, max_rank, alpha, ax):
    """
    Plot the power law curve that was fitted to the data.

    Parameters
    ----------
    curve_xmin : float
        Minimum x-bound for fitted curve
    curve_xmax : float
        Maximum x-bound for fitted curve
    max_rank : int
        Maximum word frequency rank.
    alpha : float
        Estimated alpha parameter for the power law.
    ax : matplotlib axes
        Scatter plot to which the power curve will be added.
    """
    xvals = np.arange(curve_xmin, curve_xmax)
    yvals = max_rank * (xvals**(-1 / alpha))
    ax.loglog(xvals, yvals, color='grey')


def main(args):
    "Run the program."
    set_plot_params(args.plotparams)
    df = pd.read_csv(args.infile, header=None,
                    names=('word', 'word_frequency'))
    df['rank'] = df['word_frequency'].rank(ascending=False,
                                            method='max')
    ax = df.plot.scatter(x='word_frequency', y='rank',
                         figsize=[12,6], grid=True,
                         style=args.style,
                         loglog=True,
                         xlim=args.xlim)
    word_counts = df['word_frequency'].to_numpy()
    alpha = get_power_law_params(word_counts)
    print('alpha:', alpha)

    # Since the ranks are already sorted, we can take the last
    # one instead of computer which row has the highest rank
    max_rank = df['rank'].to_numpy()[-1]

    # Use the range of the data as the boundaries
    # when drawing the power law curve
    curve_xmin = df['word_frequency'].min()
    curve_xmax = df['word_frequency'].max()

    plot_fit(curve_xmin, curve_xmax, max_rank, alpha, ax)
    mpl.pyplot.style.use(args.style)
    ax.figure.savefig(args.outfile)

    if args.saveconfig:
        with open(args.saveconfig, 'w') as dumper:
            yaml.dump(mpl.rcParams, dumper)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('infile', type=argparse.FileType('r'),
                        nargs='?', default='-',
                        help='Word count csv file name')
    parser.add_argument('--outfile', type=str,
                        default='plotcounts.png',
                        help='Output image file name')
    parser.add_argument('--xlim', type=float, nargs=2,
                        metavar=('XMIN', 'XMAX'),
                        default=None, help='X-axis bounds')
    parser.add_argument('--plotparams', type=str, default=None,
                        help='matplot lib paramters (YAML file)')
    parser.add_argument('--style', type=str, default='classic',
                        choices=mpl_plot_styles, nargs='*',
                        help='select from pre-defined matplotlib styles')
    parser.add_argument('--saveconfig', type=str, default=None,
                        help='filename to save the configs')
    args = parser.parse_args()
    print(args.saveconfig)
    main(args)

