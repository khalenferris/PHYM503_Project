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
vul_data = sys.argv[1]		 # .vul file to use
num_spec = sys.argv[2]		 # How many species to plot
plot_name = sys.argv[3] 	 # Name of plot

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

high_mix = np.argsort(avg_mix)[-int(num_spec):][::-1]
high_mix_spec = [species[i] for i in high_mix]
high_mix_val = avg_mix[high_mix]

# Plotting
plt.figure(figsize=(8,5))
plt.bar(range(int(num_spec)),high_mix_val,color='midnightblue')
plt.yscale('log')
plt.xticks(range(int(num_spec)), high_mix_spec, rotation=45, ha='right')
plt.ylabel("Average Mixing Ratio")
plt.tight_layout()

out = os.path.join(plot_dir, f"{plot_name}_most.png")
plt.savefig(out, bbox_inches='tight', dpi=300)
print(f"Bar chart saved to {out}")
sys.exit(0)
