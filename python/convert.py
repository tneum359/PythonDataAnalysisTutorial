#!/usr/bin/env python
import math

# arrays for y values
n_pos = []
n_all = []

# read all data in one shot
with open("c19.dat","r") as file:
    data = file.read()

# go through each row
pos = True
for line in data.split("\n"):
    f = line.split("\t")                                # use a comma to separate columns
    f[-1] = f[-1].replace(',','')
    if len(f)>1 and len(line)>0 and line[0] != '#':    # protect against not well formatted lines
        if pos:
            n_pos.append(float(f[-1]))
            pos = False
        else:
            n_all.append(float(f[-1]))
            pos = True

i = 0
for na,np in zip(n_all,n_pos):
    print("%d,0.0,%f,%f"%(i,np/na*100,math.sqrt(np)/na*100))
    i += 1

