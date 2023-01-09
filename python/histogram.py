#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mlp
from optparse import OptionParser

# initial settings
mlp.rcParams['axes.linewidth'] = 2

#---------------------------------------------------------------------------------------------------
def readDataFromFile(file_name): 
        
    # arrays for y values
    xs = []

    # read all data in one shot
    with open(file_name,"r") as file:
        data = file.read()

    # go through each row
    for line in data.split("\n"):
        f = line.split(',')                                # use a comma to separate columns
        if len(f)>0 and len(line)>0 and line[0] != '#':    # protect against not well formatted lines
             xs.append(float(f[0]))

    return np.array(xs)

#---------------------------------------------------------------------------------------------------
# define and get all command line arguments
parser = OptionParser()
parser.add_option("-n", "--name",  dest="name",  default='histogram',      help="name of plot")
parser.add_option("-x", "--xtitle",dest="xtitle",default='Default x title',help="x axis title")
parser.add_option("-y", "--ytitle",dest="ytitle",default='Default y title',help="y axis title")
(options, args) = parser.parse_args()

# get my data
xs = readDataFromFile("../dat/"+options.name+".dat")
print(xs)

# define the figure
plt.figure(options.name)
n, bins, patches = plt.hist(xs, 20, histtype='step', linewidth=2.0)

# give the plot some head room
plt.ylim(0,n.max()*1.1)

# make plot nicer
plt.xlabel(options.xtitle, fontsize=18)
plt.ylabel(options.ytitle, fontsize=18)

# make axis tick numbers larger
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# make sure to noe have too much white space around the plot
plt.subplots_adjust(top=0.99, right=0.99, bottom=0.13, left=0.12)

# save plot for later viewing
plt.savefig("../png/"+options.name+".png",bbox_inches='tight',dpi=400)

# show the plot for interactive use
plt.show()
print("hi")
