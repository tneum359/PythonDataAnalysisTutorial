# Introduction / jupyter

In this folder we present a number of fundamental tools that you can use to analyze your data. There are 4 basic tools which have been written to be as simple as possible but offering some reasonable flexibility with some useful parameters. To work with these jupyter notebooks you can install them in your submit directory

    ssh <user-name>@submit.mit.edu
    git clone https://github.com/JLabMit/JLabExperiments

and then access and run them on our jupyterhub server at:

    https://submit00.mit.edu/jupyter

You have to navigate to the directory where you installed the software (JLabExperiments/PythonDataAnalysisTutorial/jupyter) and run them. Data for these examples are automatically read and are in the PythonDataAnalysisTutorial/dat directory with the same trunk as the script but with the .dat extension.

## histogram

In this script we read the file histogram.dat (in PythonDataAnalysisTutorial/dat/) which contains a single column of values. Those values are read and then historgrammed.

## graph_xy

In this script we read the file graph_xy.dat (in PythonDataAnalysisTutorial/dat/) which contains a two columns of values (x,y). Those values are read and then plotted in form of an xy-graph.

## graph_xdxydy

In this script we read the file graph_xdxydy.dat (in PythonDataAnalysisTutorial/dat/) which contains a four columns of values (x,dx,y,dy), so x and y values including their uncertainties. Those values are read and then plotted in form of an xy-graph.

## fit

In this script we read generate a set of random number according to a Gaussian and then histogram them and display them. We then perform a fit where we fit a Gaussian distribution to those histogram bins.
