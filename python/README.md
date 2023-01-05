# Introduction / python

In this folder we present a number of fundamental tools that you can use to analyze your data. There are 4 basic tools which have been written to be as simple as possible but offering some reasonable flexibility at the command line. Each of the for core scripts can be called from the command line when you change to the PythonDataAnalysisTutorial/python folder.

Data for these examples are in the PythonDataAnalysisTutorial/dat directory with the same truncate as the script but with the .dat extension.

## histogram

In this script we read the file histogram.dat (in PythonDataAnalysisTutorial/dat/) which contains a single column of values. Those values are read and then historgrammed.

    cd PythonDataAnalysisTutorial/python
    ./histogram.py


## graph_xy

In this script we read the file graph_xy.dat (in PythonDataAnalysisTutorial/dat/) which contains a two columns of values (x,y). Those values are read and then plotted in form of an xy-graph.

    cd PythonDataAnalysisTutorial/python
    ./graph_xy.py

## graph_xdxydy

In this script we read the file graph_xdxydy.dat (in PythonDataAnalysisTutorial/dat/) which contains a four columns of values (x,dx,y,dy), so x and y values including their uncertainties. Those values are read and then plotted in form of an xy-graph.

    cd PythonDataAnalysisTutorial/python
    ./graph_xdxydy.py

## fit

In this script we read generate a set of random number according to a Gaussian and then histogram them and display them. We then perform a fit where we fit a Gaussian distribution to those histogram bins.

    cd PythonDataAnalysisTutorial/python
    ./fit.py
