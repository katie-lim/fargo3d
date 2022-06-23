# %%
from units import *
import re

import matplotlib.pyplot as plt
import numpy as np
# from matplotlib.collections import LineCollection
# from scipy import integrate
# from pathlib import Path

# %%

def showFigure(show: bool):
    if show:
        plt.show()
    else:
        plt.close()


def getVariableFromParFile(variableName, fileText):
    """Returns the specified variable from a .par file.

    Args:
        variableName (str): The variable to be retrieved (e.g. Nx, Ny, DT).
        fileText (str): The contents of the .par file.

    Returns:
        The value of the specified variable.
    """
    matches = re.findall(variableName + "[\s]+([\w\d\/.e-]+)", fileText)

    def convertToType(s):
        try:
            return int(s)
        except ValueError:
            try:
                return float(s)
            except:
                return s

    return convertToType(matches[0])


def getParameters(variables, parFile):
    """Returns an list of the specified variables from the specified .par file.

    Args:
        variables (list of str): An array containing the variables to be retrieved -- e.g. ["Nx", "Ny"]
        parFile (str): The path to the .par file.

    Returns:
        (list of str): An list containing the specified variables from the specified .par file.
    """

    textFile = open(parFile, 'r')
    fileText = textFile.read()
    textFile.close()

    return [getVariableFromParFile(var, fileText) for var in variables]


def loadData(dataFile, parFile, logScale, logRadialSpacing, useRealUnits=True):
    """Loads the output data contained within the specified dataFile.

    Args:
        dataFile (str): The path to the data file.
        parFile (str): The path to the .par file.
        logScale (bool): Whether to use a log scale.
        logRadialSpacing (bool): Whether the radial spacing is linear (False) or logarithmic (True).
        useRealUnits (bool): Whether to return the data in real units. Defaults to True.

    Returns:
        values, rad, azm (np.array, np.array, np.array): The output values, radial values, and azimuthal angle values.
    """
    # Load the parameter file
    x, y, Ymin, Ymax = getParameters(["Nx", "Ny", "Ymin", "Ymax"], parFile)

    # Load the data
    values = np.fromfile(dataFile).reshape(y, x).transpose()

    azm = np.linspace(0, 2*np.pi, x)

    if not logRadialSpacing:
        rad_edges = np.linspace(Ymin, Ymax, y+1)
    else:
        rad_edges = np.geomspace(Ymin, Ymax, y+1)

    rad = [0.5*(rad_edges[i] + rad_edges[i-1]) for i in range(1, y+1)]  # use the cell midpoints
    rad = np.array(rad)


    # Convert to real units
    if useRealUnits:
        rad *= R0
        values *= density_scale_factor

    if logScale:
        values = np.log10(values)

    return values, rad, azm



def plotOrbitalParameter(fileNames, parameterName, labels=["Planet 1", "Planet 2"], title=None, saveFileName=None, Ni=0, Nf=None, show=True):
    """Plots the specified orbital parameter against time for multiple setups.

    Args:
        fileNames (list of str): The paths to the orbitX.dat files to plot.
        parameterName (str): The parameter to plot -- one of: eccentricity, semiMajorAxis
        labels (list of str): Labels for each of the setups to use in the figure.
        title (str, optional): The title of the figure.
        saveFileName (str, optional): The path to save the resulting plot to. If None, the figure is not saved.
    """
    parameterName = parameterName.lower()
    plt.figure(dpi=dpi)

    # Load the data
    for i in range(len(fileNames)):
        data = np.loadtxt(fileNames[i])
        date, eccentricity, semiMajorAxis, meanAnomaly, trueAnomaly, argOfPeriastron, rotationAngle, inclination, longitude, angleOfPerihelion = data.transpose()

        # Convert to real units
        date = [convertToRealTime(time) for time in date]
        semiMajorAxis *= R0

        # Plot the data
        if parameterName == "eccentricity":
            plt.plot(date[Ni:Nf], eccentricity[Ni:Nf], label=labels[i])
        elif parameterName == "semimajoraxis":
            plt.plot(date[Ni:Nf], semiMajorAxis[Ni:Nf], label=labels[i])
        else:
            raise Exception("The parameter name " + parameterName + " is not recognised.")


    if parameterName == "eccentricity":
        plt.ylabel("eccentricity")
        plt.gca().set_ylim(bottom=0)
    elif parameterName == "semimajoraxis":
        ylabel = "semi-major axis [" + R0_unit + "]"
        plt.ylabel(ylabel)


    xlabel = "time [" + unit_of_time + "]"
    plt.xlabel(xlabel)
    if title: plt.title(title)
    plt.legend()
    plt.gcf().set_size_inches(8, 5)

    if saveFileName: plt.savefig(saveFileName, dpi=dpi)

    showFigure(show)


def getEccentricity(fileName):
    # Load the data
    data = np.loadtxt(fileName)
    date, eccentricity, semiMajorAxis, meanAnomaly, trueAnomaly, argOfPeriastron, rotationAngle, inclination, longitude, angleOfPerihelion = data.transpose()

    # Consider the last 10% of the data
    eccentricity = eccentricity[int(np.size(eccentricity)*0.9):]

    avg = np.mean(eccentricity)

    return avg



def plotPeriodRatio(fileNames, Ni=0, Nf=None, title=None, labels=None, saveFileName=None, show=True):
    plt.figure(figsize=(8,5), dpi=dpi)

    for i in range(len(fileNames) // 2):
        # Load the data
        a = np.loadtxt(fileNames[2*i])
        datea, eccentricitya, semiMajorAxisa, meanAnomaly, trueAnomaly, argOfPeriastron, rotationAngle, inclination, longitude, angleOfPerihelion = a.transpose()
        b = np.loadtxt(fileNames[2*i + 1])
        dateb, eccentricityb, semiMajorAxisb, meanAnomaly, trueAnomaly, argOfPeriastron, rotationAngle, inclination, longitude, angleOfPerihelion = b.transpose()

        # Convert to real units
        date = [convertToRealTime(datei) for datei in datea][Ni:Nf]
        semiMajorAxisa *= R0
        semiMajorAxisb *= R0

        # Make sure arrays are the same size to prevent errors while files are still being written to
        sizea, sizeb = np.size(semiMajorAxisa), np.size(semiMajorAxisb)

        if sizea < sizeb:
            semiMajorAxisb = semiMajorAxisb[0:sizea]
        elif sizeb < sizea:
            semiMajorAxisa = semiMajorAxisa[0:sizeb]


        # Plot the ratio of orbital periods as a fn of time
        ratio = np.power(semiMajorAxisb[Ni:Nf]/semiMajorAxisa[Ni:Nf], 3/2)

        if labels:
            plt.plot(date, ratio, label=labels[i])
        else:
            plt.plot(date, ratio)

        # print("Average ratio: " + ("%.4f" % np.average(ratio[-3000:])))


    plt.title(title)
    plt.xlabel("time [" + unit_of_time + "]")
    plt.ylabel("ratio of orbital periods")

    if labels:
        plt.legend()

    if saveFileName: plt.savefig(saveFileName, dpi=dpi)

    showFigure(show)

    return ratio



def calcAvgPeriodRatio(fileNames):
    # Load the data
    a = np.loadtxt(fileNames[0])
    datea, eccentricitya, semiMajorAxisa, meanAnomaly, trueAnomaly, argOfPeriastron, rotationAngle, inclination, longitude, angleOfPerihelion = a.transpose()
    b = np.loadtxt(fileNames[1])
    dateb, eccentricityb, semiMajorAxisb, meanAnomaly, trueAnomaly, argOfPeriastron, rotationAngle, inclination, longitude, angleOfPerihelion = b.transpose()

    # Convert to real units
    date = [convertToRealTime(datei) for datei in datea]
    semiMajorAxisa *= R0
    semiMajorAxisb *= R0

    # Make sure arrays are the same size to prevent errors while files are still being written to
    sizea, sizeb = np.size(semiMajorAxisa), np.size(semiMajorAxisb)

    if sizea < sizeb:
        semiMajorAxisb = semiMajorAxisb[0:sizea]
    elif sizeb < sizea:
        semiMajorAxisa = semiMajorAxisa[0:sizeb]


    # Calculate the ratio of orbital periods as a fn of time
    ratio = np.power(semiMajorAxisb/semiMajorAxisa, 3/2)

    # Consider the last 10% of the data
    ratio = ratio[int(np.size(ratio)*0.9):]

    avg = np.mean(ratio)
    stdDev = np.std(ratio)

    return (avg, stdDev)


def calcSuggestedResonance(avgPeriodRatio, stdDevPeriodRatio):
    # p,q values
    resonances = [[1, 1], [2, 1], [3, 2]]

    for (p, q) in resonances:
        idealRatio = (p + q)/p

        if (idealRatio - 0.2 < avgPeriodRatio < idealRatio + 0.2):
            if stdDevPeriodRatio < 0.1:
                resonanceName = "%d:%d" % (p + q, p)
                return (resonanceName, p, q)

    return None


def plotResonantAnglesVsTime(fileName1, fileName2, p, q, Ni=0, Nf=None, saveFileName=None, show=True):
    """Plots the resonant angles against time.

    Args:
        fileName1 (str): [description]
        fileName2 (str): [description]
        p (int): [description]
        q (int): [description]
        Ni (int, optional): [description]. Defaults to 0.
        Nf (int, optional): [description]. Defaults to None.
    """

    # Load the data
    data1 = np.loadtxt(fileName1)
    data2 = np.loadtxt(fileName2)

    date, eccentricity1, semiMajorAxis, meanAnomaly1, trueAnomaly, argOfPeriastron, rotationAngle, inclination, longitude, angleOfPerihelion1 = data1.transpose()
    date, eccentricity2, semiMajorAxis, meanAnomaly2, trueAnomaly, argOfPeriastron, rotationAngle, inclination, longitude, angleOfPerihelion2 = data2.transpose()
    time = [convertToRealTime(t) for t in date[Ni:Nf]]

    # Calculate the resonant angles
    meanLongitude1 = meanAnomaly1 + angleOfPerihelion1
    meanLongitude2 = meanAnomaly2 + angleOfPerihelion2

    phi1 = ((p+q)*meanLongitude2 - p*meanLongitude1 - q*angleOfPerihelion1) % (2*np.pi)
    phi2 = ((p+q)*meanLongitude2 - p*meanLongitude1 - q*angleOfPerihelion2) % (2*np.pi)

    # Convert to degrees
    phi1 *= (180 / np.pi)
    phi2 *= (180 / np.pi)

    # Plot the results
    plt.figure(figsize=(8,5), dpi=dpi)
    plt.scatter(time, phi1, s=1, label=r"%d $\lambda_2$ - %d $\lambda_1$ - %d $\varpi_1$" % (p+q, p, q))
    plt.scatter(time, phi2, s=1, label=r"%d $\lambda_2$ - %d $\lambda_1$ - %d $\varpi_2$" % (p+q, p, q))

    plt.xlabel("time [" + unit_of_time + "]")
    plt.ylabel("resonant angle [$^{\circ}$]")
    plt.ylim(0, 360)
    plt.xlim(0)
    plt.suptitle(fileName1 + "\n" + fileName2)
    plt.legend()

    if saveFileName: plt.savefig(saveFileName, dpi=dpi)
    showFigure(show)


def plotPolarOnAxes(axes, values, rad, azm, vmin, vmax):
    """Plots the given data on a given set of matplotlib Axes.

    Args:
        axes (matplotlib.axes.Axes): The axes to plot the data on.
        values (array of float): The data values.
        rad (array of float): The radial values.
        azm (array of float): The azimuthal values.
        logScale (bool): Whether to use a log scale.
        vmin (float): The lower bound on the colormap scale.
        vmax (float): The upper bound on the colormap scale.

    Returns:
        cax (matplotlib.contour.ContourSet): The result obtained from calling axes.contourf(). Can be used to add a colorbar.
    """
    # Fix the color scale
    if vmin == None:
        # If no limits have been given, default to the min/max of the data
        vmin, vmax = values.min(), values.max()
        if vmax == vmin:
            vmax += 1


    r, theta = np.meshgrid(rad, azm)
    levels = np.linspace(vmin, vmax, 64)
    cax = axes.contourf(theta, r, values, levels=levels, cmap="magma", extend="neither")

    # Offset the inner boundary of the disk from 0
    axes.set_ylim(0, rad[-1]) # the maximum radial value is rad[-1]
    axes.set_rorigin(-1)

    # Add a label for the units of radial distance
    label_position=axes.get_rlabel_position()
    axes.text(np.radians(label_position+11),axes.get_rmax()/1.6, R0_unit,rotation=label_position,ha='center',va='center')

    return cax


def plotPolar(fileName, parFile, logRadialSpacing, logScale=False, saveFileName=None, vmin=None, vmax=None, rotate=0, radialCutoff=None, show=True):
    """Plots the specified data file in polar coordinates.

    Taken and modified from
    https://stackoverflow.com/questions/9071084/polar-contour-plot-in-matplotlib-best-modern-way-to-do-it
    http://blog.rtwilson.com/producing-polar-contour-plots-with-matplotlib/

    Args:
        fileName (str): The path to the data file to be plotted.
        parFile (str): The path to the .par file.
        logRadialSpacing (bool): Whether the radial spacing is linear or logarithmic.
        logScale (bool, optional): Whether to use a log scale. Defaults to False.
        saveFileName (str, optional): The path to save the resulting plot to. If None, the figure is not saved.
        vmin (float, optional): The lower bound on the colormap scale.
        vmax (float, optional): The upper bound on the colormap scale.
        rotate (float, optional): The angle, in radians, to rotate the data by. Defaults to 0.
        radialCutoff (float, optional): Limits the radial range of the plot to the specified value.

    Returns:
        size ((float, float)): The size of the output figure in pixels.
    """

    # Setup axes
    fig, ax = plt.subplots(subplot_kw=dict(projection='polar'), figsize=(7,7))

    # Load and plot the data
    values, rad, azm = loadData(fileName, parFile, logScale, logRadialSpacing=logRadialSpacing)
    azm += rotate

    if radialCutoff:
        cutoffIndex = np.argmax(rad > radialCutoff)
        values = values.transpose()[:cutoffIndex].transpose()
        rad = rad[:cutoffIndex]

    cax = plotPolarOnAxes(ax, values, rad, azm, vmin=vmin, vmax=vmax)

    # Add colorbar
    cb = fig.colorbar(cax)
    label = "log(gas density / 1" + density_unit + ")" if logScale else "gas density (" + density_unit + ")"
    cb.set_label(label)

    # Calculate the time
    index = int(re.findall("([\d]+).dat", fileName)[0]) # find the index of the file so we can calculate the time
    dt, Ninterm = getParameters(["DT", "Ninterm"], parFile)
    time = index * dt * Ninterm # the time in scale-free units
    time = convertToRealTime(time) # convert to real units

    title = fileName + "\n" + "t = " + ("%.2f" % time) + " " + unit_of_time
    plt.title(title)

    if saveFileName: plt.savefig(saveFileName, dpi=dpi)

    size = fig.get_size_inches()*dpi

    showFigure(show)

    # Return the dimensions of the image so we can render the video with the same dimensions
    return size


def plotAzimuthallyAvgedSurfaceDensities(fileNames, parFiles, logRadialSpacing, logScale=False, labels=None, title=None, saveFileName=None, show=True):

    plt.figure(figsize=(8, 5), dpi=dpi)

    for i in range(len(fileNames)):
        values, rad, azm = loadData(fileNames[i], parFiles[i], False, logRadialSpacing=logRadialSpacing)
        values = values.transpose() # make the radial coordinate r the first index

        avgSurfDens = []

        for vals in values:
            avgSurfDens.append(np.average(vals))


        if logScale:
            avgSurfDens = np.log(np.array(avgSurfDens))


        if labels:
            plt.plot(rad, avgSurfDens, linewidth=2, label=labels[i])
        else:
            plt.plot(rad, avgSurfDens, linewidth=2)


    plt.xlabel("radius [" + R0_unit + "]")
    if logScale:
        plt.ylabel("log(avg surface density [" + density_unit + "])")
    else:
        plt.ylabel("avg surface density [" + density_unit + "]")
    plt.title(title)
    if labels: plt.legend()

    if saveFileName: plt.savefig(saveFileName, dpi=dpi)

    showFigure(show)


