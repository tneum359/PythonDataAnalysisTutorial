#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mlp

from scipy.stats import norm
from scipy.optimize import curve_fit
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

def uncertainties(ys,patch=False):
    # find uncertainties (simply sqrt of entries)
    # - for fitting a 0 uncertainty does not work so we set it to 1000 to avoid chi2 contribution
    sigmas = np.sqrt(ys)
    for i in range(0,len(sigmas)): # if there are zero entries we get division by zero!
        if sigmas[i] == 0 and patch:
            sigmas[i] = 1000
    return sigmas

def straight_mean_var(data):
    # mean and variance from the raw data
    mean_raw = np.mean(data)
    var_raw = np.var(data)
    print("\n-- No fit")
    print(" Nevents:  %d"%(len(data)))
    print(" Mean:     %f +- %f"%(np.mean(data),np.sqrt(np.var(data)/len(data))))
    print(" Variance: %f"%(np.var(data)))
    print(" Width:    %f"%(np.sqrt(np.var(data))))

    return mean_raw,var_raw

def gaussian(x, amplitude, mean, width):
    # Gaussian function, including a variable normalization, ready for your histogram fit

    return amplitude*g_norm/width * np.exp(-0.5*((x-mean)/width)**2)

def fit_gaussian_without(xs,ys):
    # implement a set of histogram fits
    
    x_array = np.array(xs)
    y_array = np.array(ys)

    # fit without uncertainties
    pname = ['Amplitude', 'Mean', 'Width']
    par, pcov = curve_fit(gaussian, x_array, y_array, p0=(500, 10, 2))
    print("\n== Fit without including uncertainties")
    for i in range(0,3):
        print(" P(%9s,%d): %f +- %f"%(pname[i],i,par[i],np.sqrt(pcov[i][i])))

    return par, pcov

def fit_gaussian(xs,ys):
    # implement a set of histogram fits
    
    x_array = np.array(xs)
    y_array = np.array(ys)

    # find uncertainties (simply sqrt of entries)
    sigmas = uncertainties(y_array,True) # patch uncertainties of 0
    
    # fit with uncertainties
    print("\n== Fit including uncertainties")
    pname = ['Amplitude', 'Mean', 'Width']
    par, pcov = curve_fit(gaussian, x_array, y_array, p0=(500, 10, 2), sigma=sigmas)
    for i in range(0,3):
        print(" P(%9s,%d): %f +- %f"%(pname[i],i,par[i],np.sqrt(pcov[i][i])))

    chi2,ndof = chi2_ndof(gaussian, par, x_array, y_array, sigmas)
    prob = probability(chi2,ndof)
    print(" Chi2: %f,  Ndof: %d"%(chi2,ndof))
    print(" Prob: %f"%(prob))
        
    return par, pcov, prob

def chi2_ndof(gaussian, par, x_array, y_array, sigma):
    chi2 = 0.
    ndof = len(par) * (-1.)
    for x,y,sig in zip(x_array,y_array,sigma):
        prediction = gaussian(x,par[0],par[1],par[2])
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

n_events = 500

# generate some data for this demonstration.
data = norm.rvs(20.0, 2.5, size=n_events)

# calculate variables
mean_raw,var_raw = straight_mean_var(data)

# define the figure
fig = plt.figure(options.name,figsize=(6,6))
#ns, bins, patches = plt.hist(data, 25, histtype = 'step', linewidth=2)
ns, bins, patches = plt.hist(data, 25, histtype = 'step',color='w',alpha=.01)
#ns, bins, patches = plt.hist(data, 25)

# careful bin width matters for integral
binwidth = bins[1]-bins[0]
normalize = n_events * binwidth

# plot the prediction on top
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = normalize * norm.pdf(x, mean_raw, np.sqrt(var_raw)) # make sure to normalize correctly
label = "mu= %.2f, std= %.2f" % (mean_raw, np.sqrt(var_raw))
plt.plot(x, p, 'r', linewidth=2, label=label)
# legend
leg = plt.legend(loc="upper left",frameon=False)

# prepare data for the least chi2 binned fit
xs = []
ys = []
for n,bmin in zip(ns,bins[:-1]):
    xs.append(bmin+0.5*binwidth)
    ys.append(n)

# make a marker plot
sigmas = uncertainties(ys)
plt.scatter(xs, ys, label=label,color='black')      # markers
plt.errorbar(xs,ys,yerr=sigmas,color='black',ls='none')   # error bars

# now fit the data
fit_gaussian_without(xs,ys)
par,pcov,prob = fit_gaussian(xs,ys)

ax = plt.gca()
plt.text(0.02,0.90,r'P($\chi^2$,Ndof): %4.1f%%'%(prob*100),{'color': 'b'}, transform=ax.transAxes)

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
