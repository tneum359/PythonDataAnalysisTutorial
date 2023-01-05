#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mlp

from optparse import OptionParser

# initial settings
mlp.rcParams['axes.linewidth'] = 2

#---------------------------------------------------------------------------------------------------
def readDataFromFile(file_name): 

    print(' File: %s'%(file_name))
    
    # arrays for y values
    diameters = []
    d_diameters = []
    heights = []
    d_heights = []
    volumes = []
    d_volumes = []

    # read all data in one shot
    with open(file_name,"r") as file:
        data = file.read()

    # go through each row
    for line in data.split("\n"):
        f = line.split(',')                                # use a comma to separate columns
        #print(" Len %d"%(len(f)))
        #print(f)
        if len(f)>6 and len(line)>0 and line[0] != '#':    # protect against not well formatted lines
            diameters.append(float(f[1]))
            d_diameters.append(float(f[2]))
            heights.append(float(f[3]))
            d_heights.append(float(f[4]))
            volumes.append(float(f[5]))
            d_volumes.append(float(f[6]))

    # make a hash array for easy access
    measurements = {}
    measurements['diameters'] = diameters
    measurements['d_diameters'] = d_diameters
    measurements['heights'] = heights
    measurements['d_heights'] = d_heights
    measurements['volumes'] = volumes
    measurements['d_volumes'] = d_volumes

    return measurements


#---------------------------------------------------------------------------------------------------
# define and get all command line arguments
parser = OptionParser()
parser.add_option("-n", "--name",  dest="name",  default='diameters',      help="name of plot")
parser.add_option("-x", "--xtitle",dest="xtitle",default='Default x title',help="x axis title")
parser.add_option("-y", "--ytitle",dest="ytitle",default='Default y title',help="y axis title")
(options, args) = parser.parse_args()

# get my data
measurements = readDataFromFile("coin.dat")
values = measurements[options.name]
#print(diameters)

# define the figure
plt.figure(options.name)
n, bins, patches = plt.hist(values, 20, histtype='step', linewidth=2.0)

# make plot nicer
plt.xlabel(options.xtitle, fontsize=18)
plt.ylabel(options.ytitle, fontsize=18)

# make axis tick numbers larger
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# make sure to noe have too much white space around the plot
plt.subplots_adjust(top=0.99, right=0.99, bottom=0.13, left=0.12)

# save plot for later viewing
plt.savefig(options.name+".png",bbox_inches='tight',dpi=400)

# show the plot for interactive use
plt.show()
