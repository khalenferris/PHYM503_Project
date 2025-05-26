'''
This script reads a VULCAN output (.vul) file using pickle and plots the X most abundant
chemical species.
Plots are saved in the folder assigned in vulcan_cfg.py with the default plot_dir = 'plot/'
'''

import sys
sys.path.insert(0, '../')  # including the upper level of directory for the path of modules

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.legend as lg
import vulcan_cfg
try: from PIL import Image
except ImportError:
    try: import Image
    except: vulcan_cfg.use_PIL = False
import os
import pickle

import matplotlib
matplotlib.use('Agg')

# Setting system arguments
vul_data = sys.argv[1]           # .vul file to use
num_spec = sys.argv[2]           # How many species to plot
plot_name = sys.argv[3]          # Name of plot

# Setting plot directory
plot_dir = '../' + vulcan_cfg.plot_dir
if not os.path.exists(plot_dir):
    print('The plotting directory assigned in vulcan_cfg.py does not exist.')
    print('Directory', plot_dir, "created.")
    os.mkdir(plot_dir)

# Read data
with open(vul_data, 'rb') as handle:
    data = pickle.load(handle)

# Compute average mixing ratios
ymix = data['variable']['ymix']
species = data['variable']['species']
avg_mix = np.mean(ymix, axis=0)

alt = data['atm']['zco'][1:]/1.e5
with np.errstate(invalid='ignore'):
        avg_alt = (alt[:, None] * ymix).sum(axis=0) / ymix.sum(axis=0)


high_mix = np.argsort(avg_mix)[-int(num_spec):][::-1]
high_mix_spec = [species[i] for i in high_mix]
high_mix_val = avg_mix[high_mix]
alt_val = avg_alt[high_mix]

# Plotting
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.bar(range(int(num_spec)), high_mix_val, color='midnightblue', label = 'Mixing Ratio')
ax1.set_ylabel("Average Mixing Ratio")
ax1.set_yscale('log')
ax2.plot(range(int(num_spec)), alt_val, 's', ls='None', color='red', label = 'Altitude')
ax2.plot(range(int(num_spec)), alt_val, ls = '--', alpha=0.5, color='red')
ax2.set_ylabel('Mean Altitude (km)')
ax1.set_xticks(range(int(num_spec)))
ax1.set_xticklabels(high_mix_spec, rotation=45, ha='right')
ax1.grid(True,axis='y',ls='--',alpha=0.7)
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2,l1+l2, loc='best')
plt.tight_layout()

out = os.path.join(plot_dir, f"{plot_name}.png")
plt.savefig(out, bbox_inches='tight', dpi=300)
print(f"Bar chart saved to {out}")
