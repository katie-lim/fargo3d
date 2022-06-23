#%%
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from scipy import integrate
from pathlib import Path
import os
import re

dpi = 300

# Units
R0 = 20
R0_unit = "AU"
R0_in_m = 20*1.496e11
Mstar = 1
Mstar_unit = "M_Sun"
Mstar_in_kg = 1.989e30
density_scale_factor = (Mstar_in_kg / R0_in_m**2)
density_unit = "kg/m$^2$"

unit_of_time_in_s = 3.154e7 # seconds in a year
unit_of_time = "yr"

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


def plotPolar(fileName, parFile, logRadialSpacing, logScale=False, saveFileName=None, vmin=None, vmax=None, rotate=0, radialCutoff=None):
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

    plt.show()

    # Return the dimensions of the image so we can render the video with the same dimensions
    return size

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


def findMinMax(folderName, fieldName, parFile, logScale, Nframes):
    """Returns the minimum and maximum output values in the data contained in the specified folder.

    Args:
        folderName (str): The path to the folder containing the data.
        fieldName (str): The name of the field to be used -- e.g. "gasdens"
        parFile (str): The path to the .par file used to obtain the data.
        logScale (bool): Whether to use a log scale.
        Nframes (int): The number of output files in the folder to include.

    Returns:
        vmin, vmax (float, float): The minimum and maximum output values.
    """
    vmin = None
    vmax = None

    # Initialise vmin and vmax
    dataPath = folderName + "/" + fieldName + "0.dat"
    values, rad, azm = loadData(dataPath, parFile, logScale, logRadialSpacing=False) # whether the radial spacing is linear/logarithmic doesn't matter here

    vmin, vmax = values.min(), values.max()

    # Compare to the rest of the data
    for i in range(1, Nframes+1):
        try:
            dataPath = folderName + "/" + fieldName + str(i) + ".dat"

            # Load the data
            values, rad, azm = loadData(dataPath, parFile, logScale, logRadialSpacing=False)

            # Update the min and max values
            vmin = min([vmin, values.min()])
            vmax = max([vmax, values.max()])
        except FileNotFoundError:
            print("File #%d doesn't exist. Exiting findMinMax now." % i)
            break

    return vmin, vmax


def makeVideo(framesSaveLocation, videoSaveLocation, folderName, parFile, fieldName, Nframes, logRadialSpacing, fixedScale=True, logScale=True):
    """Creates a video from the data in the specified folder.

    Args:
        framesSaveLocation (str): The folder to save the video frames to.
        videoSaveLocation (str): The path to save the video to.
        folderName (str): The path to the folder containing the data.
        parFile (str): The path to the .par file used to obtain the data.
        fieldName (str): The name of the field to be plotted (e.g. "gasdens")
        Nframes (int): The number of frames to plot.
        logRadialSpacing (bool): Whether the radial spacing is linear or logarithmic.
        fixedScale (bool, optional): Whether to keep the colormap scale fixed throughout the video. Defaults to True.
        logScale (bool, optional): Whether to use a log scale. Defaults to True.
    """
    if framesSaveLocation[-1] != "/":
        framesSaveLocation += "/"

    Path(framesSaveLocation).mkdir(parents=True, exist_ok=True) # create the save folder if it doesn't exist

    # Fix the color scale by finding the global min/max values
    vmin, vmax = None, None
    if fixedScale:
        vmin, vmax = findMinMax(folderName, fieldName, parFile, logScale, Nframes)

    # Determine the size of the image so we can render the video in the same dimensions
    size = None

    # Plot the data and save each frame
    for i in range(0, Nframes+1):
        try:
            dataPath = folderName + "/" + fieldName + str(i) + ".dat" # the path to the data file to be plotted
            saveFileName = framesSaveLocation + str(i) + ".png"

            size = plotPolar(dataPath, parFile, logRadialSpacing, logScale=logScale, saveFileName=saveFileName, vmin=vmin, vmax=vmax)
            plt.close()

            print("Frame " + str(i) + "/" + str(Nframes) + " done")
        except FileNotFoundError:
            print("File #%d doesn't exist. Creating video now." % i)
            break


    size = size.astype(int)
    videoSize = str(size[0]) + "x" + str(size[1])

    # Compile the frames into a video
    os.system("""ffmpeg -y -f lavfi -i color=c=white:s=""" + videoSize + """:r=24 -framerate 7 -i """ + framesSaveLocation + """%d.png -filter_complex "[0:v][1:v]overlay=shortest=1,format=yuv420p[out]" -map "[out]" """ + videoSaveLocation)

    print("Done! Video saved to " + videoSaveLocation)


def plotPolarMulti(fileNames, parFiles, titles=None, title=None, logScale=True, saveFileName=None, vmin=None, vmax=None):
    """Plots multiple data files on the same figure.

    When calculating the time, assumes all setups were defined with the same DT and Ninterm.

    Args:
        fileNames (list of str): A list containing paths to the data files to be plotted.
        parFiles (list of str): A list containing paths to the .par files used.
        titles (list of str, optional): A list containing the title to use for each subplot.
        title (list of str, optional): The title of the figure.
        logScale (bool, optional): Whether to use a log scale. Defaults to True.
        saveFileName (str, optional): The path the resulting plot will be saved to. If None, the figure is not saved.
        vmin (float, optional): The lower bound on the colormap scale. Defaults to the lower bound of the data.
        vmax (float, optional): The upper bound on the colormap scale. Defaults to the upper bound of the data.

    Returns:
        size ((float, float)): The size of the output figure in pixels.
    """
    Nfiles = len(fileNames)

    # Setup axes
    if Nfiles > 3:
        y = Nfiles//2 + Nfiles%2
        x = 2
    else:
        y = Nfiles
        x = 1

    fig, ax = plt.subplots(x, y, figsize=(18, 8), subplot_kw=dict(projection='polar'))
    ax = ax.flatten()

    # Load and plot each data file
    cax = None
    for i in range(Nfiles):
        values, rad, azm = loadData(fileNames[i], parFiles[i], logScale)
        cax = plotPolarOnAxes(ax[i], values, rad, azm, vmin=vmin, vmax=vmax)

        if titles:
            ax[i].title.set_text(titles[i])

    fig.tight_layout()
    fig.subplots_adjust(right=0.8)

    # Add colorbar
    cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
    cbar = fig.colorbar(cax, cax=cbar_ax)
    label = "log(gas density / 1" + density_unit + ")" if logScale else "gas density (" + density_unit + ")"
    cbar.set_label(label)

    # Calculate the time
    index = int(re.findall("([\d]+).dat", fileNames[0])[0]) # find the index of the file so we can calculate the time
    dt, Ninterm = getParameters(["DT", "Ninterm"], parFiles[0])
    time = index * dt * Ninterm # the time in scale-free units
    time = convertToRealTime(time) # convert to real units

    timeText = "t = " + ("%.2f" % time) + " " + unit_of_time
    if title:
        plt.suptitle(title + "\n" + timeText)
    else:
        plt.suptitle(timeText)

    if saveFileName: plt.savefig(saveFileName, dpi=dpi)

    size = fig.get_size_inches()*dpi

    plt.show()

    # Return the dimensions of the image so we can render the video with the same dimensions
    return size


def makeVideoMulti(framesSaveLocation, videoSaveLocation, folderNames, parFiles, fieldName, Nframes, titles=None, title=None, logScale=True):
    """Creates a video from multiple setups, plotting the data in the specified folders on the same figure.

    Args:
        framesSaveLocation (str): The folder to save the video frames to.
        videoSaveLocation (str): The path to save the video to.
        folderNames (list of str): A list containing paths to the folders containing the data files.
        parFiles (list of str): A list containing paths to the .par files used.
        fieldName (str): The name of the field to be plotted (e.g. "gasdens")
        Nframes (int): The number of frames to plot.
        titles (list of str, optional): A list containing the title to use for each subplot.
        title (list of str, optional): The title of the figure.
        logScale (bool, optional): Whether to use a log scale. Defaults to True.
    """

    Nplots = len(folderNames)
    if framesSaveLocation[-1] != "/":
        framesSaveLocation += "/"

    Path(framesSaveLocation).mkdir(parents=True, exist_ok=True) # create the save folder if it doesn't exist

    # Fix the color scale by finding the global min/max values
    vmin, vmax = findMinMax(folderNames[0], fieldName, parFiles[0], logScale, Nframes)
    for i in range(1, Nplots):
        vmini, vmaxi = findMinMax(folderNames[i], fieldName, parFiles[i], logScale, Nframes)

        vmin, vmax = min(vmin, vmini), max(vmax, vmaxi)

    # Determine the size of the image so we can render the video in the same dimensions
    size = None

    # Plot the data and save each frame
    for i in range(0, Nframes+1):
        files = [folderNames[j] + "/" + fieldName + str(i) + ".dat" for j in range(Nplots)]
        saveFileName = framesSaveLocation + str(i) + ".png"

        size = plotPolarMulti(files, parFiles, titles=titles, title=title, logScale=logScale, saveFileName=saveFileName, vmin=vmin, vmax=vmax)
        plt.close()

        print("Frame " + str(i) + "/" + str(Nframes) + " done")

    size = size.astype(int)
    videoSize = str(size[0]) + "x" + str(size[1])

    # Compile the frames into a video
    os.system("""ffmpeg -y -f lavfi -i color=c=white:s=""" + videoSize + """:r=24 -framerate 7 -i """ + framesSaveLocation + """%d.png -filter_complex "[0:v][1:v]overlay=shortest=1,format=yuv420p[out]" -map "[out]" """ + videoSaveLocation)

    print("Done! Video saved to " + videoSaveLocation)


def calcOrbitalPeriodInRealUnits(semiMajorAxisInM=1.496e11):
    """Returns the orbital period in real units of a planet orbiting the central star with the specified semi-major axis.

    Args:
        semiMajorAxisInM (float): The planet's semi-major axis in metres.

    Returns:
        orbitalPeriod (float): The planet's orbital period in the user-defined time unit.
    """
    orbitalPeriod = 2*np.pi * np.sqrt((semiMajorAxisInM)**3 / (6.67e-11 * Mstar_in_kg)) # calculate the orbital period in seconds using Kepler's 3rd law
    orbitalPeriod /= unit_of_time_in_s    # convert to the chosen time unit

    return orbitalPeriod


def plotOrbitalParameter(fileNames, parameterName, labels, title=None, saveFileName=None, Ni=0, Nf=None):
    """Plots the specified orbital parameter against time for multiple setups.

    Args:
        fileNames (list of str): The paths to the orbitX.dat files to plot.
        parameterName (str): The parameter to plot -- one of: eccentricity, semiMajorAxis
        labels (list of str): Labels for each of the setups to use in the figure.
        title (str, optional): The title of the figure.
        saveFileName (str, optional): The path to save the resulting plot to. If None, the figure is not saved.
    """
    parameterName = parameterName.lower()

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

    plt.show()


def plotResonantAngles(fileName1, fileName2, p, q, Ni=0, Nf=None, useColor=False):
    """Plots e_i sin(theta_i) against e_i cos(theta_i).

    Args:
        fileName1 (str): [description]
        fileName2 (str): [description]
        p (int): [description]
        q (int): [description]
        Ni (int, optional): [description]. Defaults to 0.
        Nf (int, optional): [description]. Defaults to None.
        useColor (bool, optional): [description]. Defaults to False.
    """
    # Load the data
    data1 = np.loadtxt(fileName1)
    data2 = np.loadtxt(fileName2)

    date, eccentricity1, semiMajorAxis, meanAnomaly1, trueAnomaly, argOfPeriastron, rotationAngle, inclination, longitude, angleOfPerihelion1 = data1.transpose()
    date, eccentricity2, semiMajorAxis, meanAnomaly2, trueAnomaly, argOfPeriastron, rotationAngle, inclination, longitude, angleOfPerihelion2 = data2.transpose()

    # Calculate the resonant angles
    meanLongitude1 = meanAnomaly1 + angleOfPerihelion1
    meanLongitude2 = meanAnomaly2 + angleOfPerihelion2

    phi1 = (p+q)*meanLongitude2 - p*meanLongitude1 - q*angleOfPerihelion1
    phi2 = (p+q)*meanLongitude2 - p*meanLongitude1 - q*angleOfPerihelion2

    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(10,5))


    # create first plot
    x = (eccentricity1*np.cos(phi1))[Ni:Nf]
    y = (eccentricity1*np.sin(phi1))[Ni:Nf]
    t = date[Ni:Nf]

    if useColor:
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        lc = LineCollection(segments, cmap=plt.get_cmap('jet'))
        lc.set_array(t)
        lc.set_linewidth(2)

        ax1.add_collection(lc)

        ax1.set_xlim(x.min(), x.max())
        ymin = y.min()
        ymax = y.max()
    else:
        ax1.plot(x, y)


    ax1.set_xlabel(r"$e_1\cos(\theta_1)$")
    ax1.set_ylabel(r"$e_1\sin(\theta_1)$")


    # create second plot
    x = (eccentricity2*np.cos(phi2))[Ni:Nf]
    y = (eccentricity2*np.sin(phi2))[Ni:Nf]
    t = date[Ni:Nf]

    if useColor:
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        lc = LineCollection(segments, cmap=plt.get_cmap('jet'))
        lc.set_array(t)
        lc.set_linewidth(2)

        ax2.add_collection(lc)

        ax2.set_xlim(x.min(), x.max())
        ymin = min(ymin, y.min())
        ymax = max(ymax, y.max())
        ax2.set_ylim(ymin, ymax)
    else:
        ax2.plot(x, y)

    ax2.set_xlabel(r"$e_2\cos(\theta_2)$")
    ax2.set_ylabel(r"$e_2\sin(\theta_2)$")

    plt.suptitle(fileName1 + "\n" + fileName2)
    plt.show()


def plotResonantAnglesVsTime(fileName1, fileName2, p, q, Ni=0, Nf=None):
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
    plt.figure(figsize=(8,5))
    plt.scatter(time, phi1, s=1, label=r"%d $\lambda_2$ - %d $\lambda_1$ - %d $\varpi_1$" % (p+q, p, q))
    plt.scatter(time, phi2, s=1, label=r"%d $\lambda_2$ - %d $\lambda_1$ - %d $\varpi_2$" % (p+q, p, q))

    plt.xlabel("time [" + unit_of_time + "]")
    plt.ylabel("resonant angle [$^{\circ}$]")
    plt.ylim(0, 360)
    plt.xlim(0)
    plt.suptitle(fileName1 + "\n" + fileName2)
    plt.legend()
    plt.show()


def convertToRealTime(t):
    """Converts a given time in scale-free units to real units.

    Args:
        t (float): A time in scale free-units.
    Returns:
        The time in real units.
    """

    return t/(2*np.pi) * calcOrbitalPeriodInRealUnits(R0_in_m)


def integrateDensity(fileName, parFile, logRadialSpacing, useRealUnits=False, ri=0, rf=None):
    """Integrate the surface density of the disk over area, returning the mass of the disk within the specified radial region.

    Args:
        fileName (str): The path to the gasdens.dat file.
        parFile (str): The path to the .par file used.
        logRadialSpacing (bool): Whether the radial spacing is linear or logarithmic.
        useRealUnits (bool, optional): Whether to return the mass in real units. Defaults to False.
        ri (int, optional): The index of the radial coordinate to use as the lower limit of integration. Defaults to 0 (the inner boundary of the disk).
        rf (int, optional): The index of the radial coordinate to use as the upper limit of integration. Defaults to None (the outer boundary of the disk).

    Returns:
        The mass of the disk within the specified radial region.
    """
    # Load the data
    sigma, rad, azm = loadData(fileName, parFile, False, useRealUnits=False, logRadialSpacing=logRadialSpacing)

    if useRealUnits:
        rad *= R0_in_m
        sigma *= density_scale_factor

    integrand = sigma.transpose() # make the radial coordinate r the first index

    # Limit to the specified radial region
    integrand = integrand[ri:rf]
    rad = rad[ri:rf]

    for i in range(np.size(rad)):
        integrand[i] *= rad[i] # give the integrand the proper form: \int \Sigma r dr d\theta


    result = integrate.simps(integrate.simps(integrand, azm), rad)

    return result


def plotPeriodRatio(fileNames, Ni=0, Nf=None, title=None, labels=None):
    plt.figure(figsize=(8,5))

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

        print("Average ratio: " + ("%.4f" % np.average(ratio[-3000:])))


    plt.title(title)
    plt.xlabel("time [" + unit_of_time + "]")
    plt.ylabel("ratio of orbital periods")

    if labels:
        plt.legend()

    plt.show()

    return ratio


def plotAzimuthallyAveragedSurfaceDensities(fileNames, parFiles, logRadialSpacing, logScale=False, labels=None, title=None):
    plt.figure(figsize=(10, 7))

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
    plt.show()

# %%
