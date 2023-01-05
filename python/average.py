#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mlp

from scipy.stats import norm
from scipy.optimize import curve_fit
from scipy.optimize import leastsq
from scipy import stats

from optparse import OptionParser

g_norm = 1.0/np.sqrt(2*np.pi)

#---------------------------------------------------------------------------------------------------
# define and get all command line arguments
parser = OptionParser()
parser.add_option("-n", "--name",  dest="name",  default='fit',            help="name of plot")
parser.add_option("-x", "--xtitle",dest="xtitle",default='Default x title',help="x axis title")
parser.add_option("-y", "--ytitle",dest="ytitle",default='Default y title',help="y axis title")
(options, args) = parser.parse_args()

def constant(x, c):
    # Gaussian function, including a variable normalization, ready for your histogram fit
    return c

def fit_constant(xs,dxs):
    # implement a set of histogram fits
    
    x_array = np.array(xs)
    dx_array = np.array(dxs)
    
    # fit with uncertainties
    print("\n== Fit including uncertainties")
    pname = ['Constant']
    #par, pcov = curve_fit(constant, x_array, x_array, p0=(5), sigma=dx_array)
    par, pcov = leastsq(constant,p0 , args=(x_array, x_array), sigma=dx_array)

    print(par)
    print(pcov)
    
    s_sq = (constant(par, x_array)**2).sum()/(len(x_array)-len(par))
    print(s_sq)
    pcov = s_sq * pcov

    for i in range(0,1):
        print(" P(%9s,%d): %f +- %f"%(pname[i],i,par[i],np.sqrt(pcov[i][i])))

    chi2,ndof = chi2_ndof(constant, par, x_array, x_array, dx_array)
    prob = probability(chi2,ndof)
    print(" Chi2: %f,  Ndof: %d"%(chi2,ndof))
    print(" Prob: %f"%(prob))
        
    return par, pcov, prob

def chi2_ndof(constant, par, x_array, y_array, sigma):
    chi2 = 0.
    ndof = len(par) * (-1.)
    for x,y,sig in zip(x_array,y_array,sigma):
        prediction = constant(x,par[0])
        #print(" x: %f,  y: %f,  sig: %f, -- prediction: %f"%(x,y,sig,prediction))
        if sig>0: # make sure we do not divide by zero
            dChi2 = (y-prediction)*(y-prediction)/sig/sig
            chi2 += dChi2
            ndof += 1
            #print("dChi2: %f"%(dChi2))
        else:
            print("WARNING - sigma=0: x: %f,  y: %f,  sig: %f, -- prediction: %f"%(x,y,sig,prediction))
    return chi2, ndof

def probability(chi2,ndof):
    return (1.0 - stats.chi2.cdf(chi2,ndof))

#---------------------------------------------------------------------------------------------------
def readDataFromFile(file_name): 
        
    # arrays for y values
    xs = []
    dxs = []

    # read all data in one shot
    with open(file_name,"r") as file:
        data = file.read()

    # go through each row
    for line in data.split("\n"):
        f = line.split(',')                                # use a comma to separate columns
        if len(f)>0 and len(line)>0 and line[0] != '#':    # protect against not well formatted lines
             xs.append(float(f[0]))
             dxs.append(float(f[1]))

    return xs,dxs

xs,dxs = readDataFromFile(options.name+".dat")

print(xs)
print(dxs)

par,pcov,prob = fit_constant(xs,dxs)

##mean_raw,var_raw = straight_mean_var(data)

#
## define the figure
#fig = plt.figure(options.name,figsize=(6,6))
##ns, bins, patches = plt.hist(data, 25, histtype = 'step', linewidth=2)
#ns, bins, patches = plt.hist(data, 25, histtype = 'step',color='w',alpha=.01)
##ns, bins, patches = plt.hist(data, 25)
#
## careful bin width matters for integral
#binwidth = bins[1]-bins[0]
#normalize = n_events * binwidth
#
## plot the prediction on top
#xmin, xmax = plt.xlim()
#x = np.linspace(xmin, xmax, 100)
#p = normalize * norm.pdf(x, mean_raw, np.sqrt(var_raw)) # make sure to normalize correctly
#label = "mu= %.2f, std= %.2f" % (mean_raw, np.sqrt(var_raw))
#plt.plot(x, p, 'r', linewidth=2, label=label)
## legend
#leg = plt.legend(loc="upper left",frameon=False)
#
## prepare data for the least chi2 binned fit
#xs = []
#ys = []
#for n,bmin in zip(ns,bins[:-1]):
#    xs.append(bmin+0.5*binwidth)
#    ys.append(n)
#
## make a marker plot
#sigmas = uncertainties(ys)
#plt.scatter(xs, ys, label=label,color='black')      # markers
#plt.errorbar(xs,ys,yerr=sigmas,color='black',ls='none')   # error bars
#
## now fit the data
#fit_gaussian_without(xs,ys)
#par,pcov,prob = fit_gaussian(xs,ys)
#
#ax = plt.gca()
#plt.text(0.02,0.90,r'P($\chi^2$,Ndof): %4.1f%%'%(prob*100),{'color': 'b'}, transform=ax.transAxes)
#
## make plot nicer
#plt.xlabel(options.xtitle, fontsize=18)
#plt.ylabel(options.ytitle, fontsize=18)
#
## make axis tick numbers larger
#plt.xticks(fontsize=14)
#plt.yticks(fontsize=14)
#
## make sure to noe have too much white space around the plot
#plt.subplots_adjust(top=0.99, right=0.99, bottom=0.13, left=0.12)
#
## save plot for later viewing
#plt.savefig(options.name+".png",bbox_inches='tight',dpi=400)
#
## show the plot for interactive use
#plt.show()
#
