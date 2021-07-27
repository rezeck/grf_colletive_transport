#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import scipy.stats
import sys
from tqdm import tqdm


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h


print(len(sys.argv))
filenames = sys.argv[1:]
print(filenames)
datas = []

for filename in tqdm(filenames):
    print("Reading the file: {}".format(filename))
    datas.append(np.load(filename))


fig, axs = plt.subplots(len(filenames), sharex=True, sharey=False,
                        gridspec_kw={'hspace': 0.1})

robots = [2, 4, 10, 20]
threshold = 0.1
for i in range(0, len(filenames)):
    axs[i].set_rasterized(True)
    ax = axs[i]
    color = 'tab:blue'
    data = datas[i]
    # STATS
    lower = data[np.argmax(data[:, 2] < threshold), 0]
    mean_t = data[np.argmax(data[:, 1] < threshold), 0]
    upper = data[np.argmax(data[:, 3] < threshold), 0]
    m_std = ((upper-mean_t)+(mean_t-lower))/2.0
    print("File: {} - {} +- {}".format(filenames[i], mean_t, m_std))
    ###
    ax.plot(data[:, 0], data[:, 5], "--",
            color=color, linewidth=0.2, alpha=0.5)
    ax.plot(data[:, 0], data[:, 6], "--",
            color=color, linewidth=0.2, alpha=0.5)
    ax.plot(data[:, 0], data[:, 4],
            label='Object velocity (cm/s)', color=color)
    ax.plot([], [], label='Distance to goal (m)', color='tab:orange')
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
    if i == 1:
        ax.set_ylabel('Velocity (cm/s)',  fontsize=12, y=-0.08)
    ax.tick_params(axis='y')
    ax.set_ylim([0, 1.7])

    ax2 = ax.twinx()
    ax2.set_rasterized(True)
    color = 'tab:orange'
    if i == 1:
        ax2.set_ylabel('Distance (m)',  fontsize=12,  y=-0.02)
    ax2.plot(data[:, 0], data[:, 2], "--",
             color=color, linewidth=0.8, alpha=1.0)
    ax2.plot(data[:, 0], data[:, 3], "--",
             color=color, linewidth=0.8, alpha=1.0)
    ax2.plot([], [], label=r'$|\mathcal{R}| = $' +
             str(robots[i]), color="white", marker=".")
    ax2.legend(handletextpad=-0.1, handlelength=0)
    ax2.plot(data[:, 0], data[:, 1], label='Distance to goal', color=color)
    ax2.tick_params(axis='y')
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax2.set_ylim([0, 1.8])


# axs[0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
    #   ncol=3, fancybox=True, shadow=True)
axs[0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.40),
              ncol=2, fancybox=False, shadow=False)
# axs[0].set_title("Scalability of the Swarm", y=1.30,fontsize=16)
axs[-1].set_xlabel('Time (seconds)', fontsize=12)


plt.savefig("scalability.pdf", dpi=200)
plt.show()
