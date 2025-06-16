'''
This script reads a number of VULCAN output (.vul) files using pickle and plots the species mixing
ratios as a function of pressure/height to compare results.
Plots are saved in the folder assigned in vulcan_cfg.py, with the default plot_dir= 'plot/'
'''

import sys
sys.path.insert(0, '../') # including the upper level of directory for the path of modules

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

# swtich for plot
if '-h' in sys.argv: use_height = True
else: use_height = False

# Setting the 2nd input argument as the species names to be plotted (comma separated)
plot_spec = sys.argv[1]

if plot_spec == 'default':
    plot_spec = 'CO,CO2,H2O,HCN,H2O_l_s,CH4,C2H6'
if plot_spec == 'pbchem':
    plot_spec == 'HCN,H2CO'

# Setting the 3rd input argument as the name of the output file
plot_name = sys.argv[3]

# Setting the 4th input argument as the number of .vul files to plot
num_plots = int(sys.argv[4])

# Setting the 5th - nth input argument as the .vul files to plot
vul_input = []
for i in range(num_plots):
    vul_input.append = sys.argv[i+5]

plot_dir = '../' + vulcan_cfg.plot_dir
# Checking if plot folder exists
if not os.path.exists(plot_dir):
    print('The plotting directory assigned in vulcan_cfg.py does not exist.')
    print('Directory', plot_dir, 'created.')
    os.mkdir(plot_dir)

# Taking user input species and splitting into separate strings and then converting the list to a tuple
plot_spec = tuple(plot_spec.split(','))
nspec = len(plot_spec)

# These are the "Tableau 20" colors as RGB.
tableau20 = [(31, 119, 180),(255, 127, 14),(44, 160, 44),(214, 39, 40),(148, 103, 189),(140, 86, 75), (227, 119, 194),(127, 127, 127),(188, 189, 34),(23, 190, 207),\
(174, 199, 232),(255, 187, 120),(152, 223, 138),(255, 152, 150),(197, 176, 213),(196, 156, 148),(247, 182, 210),(199, 199, 199),(219, 219, 141),(158, 218, 229)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

# tex labels for plotting
tex_labels = {'H':'H','H2':'H$_2$','O':'O','OH':'OH','H2O':'H$_2$O','CH':'CH','C':'C','CH2':'CH$_2$','CH3':'CH$_3$','CH4':'CH$_4$','HCO':'HCO','H2CO':'H$_2$CO', 'C4H2':'C$_4$H$_2$',\
'C2':'C$_2$','C2H2':'C$_2$H$_2$','C2H3':'C$_2$H$_3$','C2H':'C$_2$H','CO':'CO','CO2':'CO$_2$','He':'He','O2':'O$_2$','CH3OH':'CH$_3$OH','C2H4':'C$_2$H$_4$','C2H5':'C$_2$H$_5$','C2H6':'C$_2$H$_6$','CH3O': 'CH$_3$O'\
,'CH2OH':'CH$_2$OH','N2':'N$_2$','NH3':'NH$_3$', 'NO2':'NO$_2$','HCN':'HCN','NO':'NO', 'NO2':'NO$_2$' }

color_index = 0
for color_index, sp in enumerate(plot_spec):
    if color_index == len(tableau20):
        tableau20.append(tuple(np.random.rand(3)))

for i in range(num_plots):
    f'vul_data_{i}' = pickle.load(vul_input[i])
    f'vul_spec_{i}' = vul_data_{i}['variable'][species]

if use_height == False:
    plt.plot(vul_data_{i}['variable']['ymix'][:,vul_spec_{i}.index(sp)], vul_data_{i}['atm']['pco']/1.e6)
else:
    plt.plot(vul_data_{i}['variable']['ymix'][:,vul_spec_{i}.index(sp)], vul_data_{i}['atm']['zco'][1:]/1.e5)

if use_height == False:
    plt.gca().set_yscale('log')
    plt.gca().invert_yaxis()
    plt.ylim((vul_data_1['atm']['pco'][0]/1e6,vul_data_1['atm']['pco'][-1]/1e6))
    plt.ylabel("Pressure (bar)")
else:
    plt.ylim((vul_data_1['atm']['zmco'][0]/1e5,vul_data_1['atm']['zmco'][-1]/1e5))
    plt.ylabel("Altitude (km)")
plt.xlabel("Mixing Ratio")

plt.gca().set_xscale('log')
plt.xlim((1.E-12, 1.e-2))

output_pdf = os.path.abspath(os.path.join(plot_dir, f"{plot_name}.pdf"))
plt.savefig(output_pdf, bbox_inches='tight',dpi=300)
print(f"Saved plot to {output_pdf}")