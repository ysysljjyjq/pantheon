#!/usr/bin/env python

import argparse
import subprocess
import os
import numpy as np
import pantheon_helpers
from tabulate import tabulate
import plot_summary
from helpers.pantheon_help import check_call

def fmt(number):
    return '{:.2f}'.format(number)

def get_difference(metric_1, metric_2):
    return '{:+.1%}'.format(((metric_2 - metric_1)) / metric_1)


parser = argparse.ArgumentParser()

parser.add_argument('experiment_1',
                    help='Logs folder, xz archive, or archive url from a pantheon run')
parser.add_argument('experiment_2',
                    help='Logs folder, xz archive, or archive url from a pantheon run')

args = parser.parse_args()

experiments = [args.experiment_1, args.experiment_2]
experiment_dirs = []
for experiment in experiments:
    if experiment.endswith('.tar.xz'):
        if experiment.startswith('https://'):
            check_call(['wget', experiment])
            experiment = experiment[8:] # strip https://
            experiment = experiment.split('/')[-1] # strip url path
        check_call(['tar', 'xJf', experiment])
        experiment = experiment[:-7] # strip .tar.xz
    experiment_dirs.append(experiment)


exp1_data = plot_summary.PlotSummary(True, False, experiment_dirs[0]).plot_summary()
exp2_data = plot_summary.PlotSummary(True, False, experiment_dirs[1]).plot_summary()

exp_1_schemes = set(exp1_data.keys())
exp_2_schemes = set(exp2_data.keys())
common_schemes = exp_1_schemes & exp_2_schemes 

throughput_lines = []
delay_lines = []

for scheme in common_schemes:
    exp1_tputs, exp1_delays = [x[0] for x in exp1_data[scheme]], [x[1] for x in exp1_data[scheme]]
    exp2_tputs, exp2_delays = [x[0] for x in exp2_data[scheme]], [x[1] for x in exp2_data[scheme]]

    exp1_runs = len(exp1_tputs)
    exp2_runs = len(exp2_tputs)

    exp1_throughput_mean = np.mean(exp1_tputs)
    exp2_throughput_mean = np.mean(exp2_tputs)
    exp1_throughput_std = np.std(exp1_tputs)
    exp2_throughput_std = np.std(exp2_tputs)

    throughput_lines.append([scheme, exp1_runs, exp2_runs, 'throughput (Mbit/s)', fmt(exp1_throughput_mean), fmt(exp2_throughput_mean), get_difference(exp1_throughput_mean, exp2_throughput_mean),
            fmt(exp1_throughput_std), fmt(exp2_throughput_std), get_difference(exp1_throughput_std, exp2_throughput_std)])

    exp1_delay_mean = np.mean(exp1_delays)
    exp2_delay_mean = np.mean(exp2_delays)
    exp1_delay_std = np.std(exp1_delays)
    exp2_delay_std = np.std(exp2_delays)

    delay_lines.append([scheme, exp1_runs, exp2_runs, '95th percentile delay (ms)', fmt(exp1_delay_mean), fmt(exp2_delay_mean), get_difference(exp1_delay_mean, exp2_delay_mean),
            fmt(exp1_delay_std), fmt(exp2_delay_std), get_difference(exp1_delay_std, exp2_delay_std)])

output_headers = ['scheme', 'exp 1 runs', 'exp 2 runs', 'aggregate metric', 'mean 1', 'mean 2', '% difference', 'std dev 1', 'std dev 2', '% difference']

print('Comparison of: %s and %s' % (experiment_dirs[0], experiment_dirs[1]))
print tabulate(throughput_lines + delay_lines, headers=output_headers)
