'''
This script plots altitude against Kzz given a PTK profile. 
Plots are saved in the folder assigned in vulcan_cfg.py, with the default plot_dir = 'plot/'
'''

import sys
sys.path.insert(0, '../') # including the upper level of directory for the path  of modules

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.legend as lg
import vulcan_cfg
try: from PIL import image
except ImportError:
	try: import Image
	except: vulcan_cfg.use_PIL = False
import os
import pickle

import matplotlib
matplotlib.use('Agg')

vul_data = sys.argv[1]
plot_name = sys.argv[2]
plot_dir = '../' + vulcan_cfg.plot_dir

colors = ['c','b','g','r','m','y','k','orange','pink','grey','darkred','darkblue','salmon','chocolate','steelblue','plum','hotpink']

tex_labels = {'H':'H','H2':'H$_2$','O':'O','OH':'OH','H2O':'H$_2$O','CH':'CH','C':'C','CH2':'CH$_2$','CH3':'CH$_3$','CH4':'CH$_4$','HCO':'HCO','H2CO':'H$_2$CO', 'C4H2':'C$_4$H$_2$',\
'C2':'C$_2$','C2H2':'C$_2$H$_2$','C2H3':'C$_2$H$_3$','C2H':'C$_2$H','CO':'CO','CO2':'CO$_2$','He':'He','O2':'O$_2$','CH3OH':'CH$_3$OH','C2H4':'C$_2$H$_4$','C2H5':'C$_2$H$_5$','C2H6':'C$_2$H$_6$','CH3O': 'CH$_3$O'\
,'CH2OH':'CH$_2$OH','N2':'N$_2$','NH3':'NH$_3$', 'NO2':'NO$_2$','HCN':'HCN','NO':'NO', 'NO2':'NO$_2$' }

with open(vul_data, 'rb') as handle:
	data = pickle.load(handle)

color_index = 0
vulcan_spec = data['variable']['species']


plt.plot(data['atm']['Kzz'], data['atm']['zco'][1:-1]/1.e5, ls='-',lw=2,color='black')
plt.xlabel(r'Eddy Diffusion Coefficient ($\mathrm{cm}^2\,\mathrm{s}^{-1}$)')
plt.ylabel('Altitude (km)')
plt.gca().set_xscale('log')
plt.minorticks_on()
plt.tick_params(which='minor', length=4)
plt.grid(True, linestyle='--', linewidth=0.5)
plt.xlim(10e2,10e5)
plt.ylim(0,65)

output_png = os.path.abspath(os.path.join(plot_dir, f"{plot_name}.png"))
plt.savefig(output_png, bbox_inches='tight', dpi=300)
print(f"Saved plot to {output_png}")
