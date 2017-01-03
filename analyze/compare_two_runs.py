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
 return '%.1f' % number

def get_difference(metric_1, metric_2):
    return (100. * abs(metric_1 - metric_2)) / metric_1


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

    exp1_mean_throughput = np.mean(exp1_tputs)
    exp2_mean_throughput = np.mean(exp2_tputs)

    throughput_lines.append([scheme, 'throughput (Mbit/s)', fmt(exp1_mean_throughput),
               fmt(exp2_mean_throughput),
               fmt(get_difference(exp1_mean_throughput, exp2_mean_throughput))])
    exp1_mean_delay = np.mean(exp1_delays)
    exp2_mean_delay = np.mean(exp2_delays)

    delay_lines.append([scheme, '95th percentile delay (ms)', fmt(exp1_mean_delay),
               fmt(exp2_mean_delay),
               fmt(get_difference(exp1_mean_delay, exp2_mean_delay))])

output_headers = ['scheme', 'aggregate metric', experiment_dirs[0], experiment_dirs[1],
                  'difference %']

print tabulate(throughput_lines + delay_lines, headers=output_headers)
