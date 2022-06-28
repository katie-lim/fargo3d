# %%
from analysis.utilities import *
from analysis.plot import *
from os.path import exists
import os


def getPlotSavePath(plotName, setupName):
    return "analysis/plots/%s/%s_%s.png" % (plotName, plotName, setupName)


def getResultsTemplate():
    f = open("analysis/simulation_results_template.md", "r")
    template = f.read()
    f.close()

    return template


def plotResultsForSimulation(setupName, show=True):
    parFile = "setups/fargo/%s.par" % setupName

    orbit0 = "outputs/%s/orbit0.dat" % setupName
    orbit1 = "outputs/%s/orbit1.dat"% setupName
    files = [orbit0, orbit1]

    lastOutputNumber = findLastOutputNumber(setupName)
    lastGasdens = "outputs/%s/gasdens%d.dat" % (setupName, lastOutputNumber)


    # Plot results
    plotOrbitalParameter(files, "semiMajorAxis", saveFileName=getPlotSavePath("semi_major_axes", setupName), show=show)

    plotOrbitalParameter(files, "eccentricity", saveFileName=getPlotSavePath("eccentricity", setupName), show=show)

    plotPeriodRatio(files, saveFileName=getPlotSavePath("period_ratio", setupName), show=show)

    periodRatio, stdDevPeriodRatio = calcAvgPeriodRatio(files)

    suggestedResonance = calcSuggestedResonance(periodRatio, stdDevPeriodRatio)

    if suggestedResonance is not None:
        resonanceName, p, q = suggestedResonance

        plotResonantAnglesVsTime(orbit0, orbit1, p, q, saveFileName=getPlotSavePath("resonant_angles", setupName), show=show)

        suggestedResonance = resonanceName
    else:
        suggestedResonance = ""


    plotPolar(lastGasdens, parFile, True, saveFileName=getPlotSavePath("gas_density", setupName), show=show)

    plotAzimuthallyAvgedSurfaceDensities([lastGasdens], [parFile], True, saveFileName=getPlotSavePath("azimuthally_avged_surface_density", setupName), show=show)

    return (periodRatio, stdDevPeriodRatio, suggestedResonance, orbit0, orbit1)


def writeSimulationResultsToFile(setupName, periodRatio, stdDevPeriodRatio, suggestedResonance, orbit0, orbit1):

    sim: Simulation = getSimulationFromLabel(setupName)
    simulationParams = sim.keys()
    simulationParamValues = sim.values()

    e1 = getEccentricity(orbit0)
    e2 = getEccentricity(orbit1)


    path = "analysis/%s.md" % setupName

    def processLine(line):
        parameters = ["period_ratio", "suggested_resonance", "e1", "e2"]
        values = ["%.2f ± %.2f" % (periodRatio, stdDevPeriodRatio), suggestedResonance, "%.3f" % e1, "%.3f" % e2]

        # Add results
        for (param, value) in zip(parameters, values):
            if line.startswith("%s::" % param):
                return "%s:: %s" % (param, value)


        # Add simulation parameters
        for (param, value) in zip(simulationParams, simulationParamValues):
            if line.startswith("%s:" % param):
                return "%s: %s" % (param, value)


        return line.rstrip()


    # Keep any notes written to the file
    fileExists = exists(path)

    if (fileExists):
        with open(path, "r") as file:
            lines = file.readlines()
    else:
        template = getResultsTemplate().replace("{{setup_name}}", setupName)
        lines = template.splitlines()


    # Update the simulation results
    processedLines = [processLine(line) for line in lines]


    with open(path, "w", encoding="utf-8") as file:
        file.writelines([line + '\n' for line in processedLines])


def processSimulation(setupName):
    res = plotResultsForSimulation(setupName, show=False)
    writeSimulationResultsToFile(setupName, *res)

    return


# %%
# setupName = "2-jupiter-2.5x-sigma0-0.001-alpha"

# res = processSimulation(setupName)

# %%
def getListOfSimulationOutputs():
    root = "outputs"

    dirList = [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item)) ]

    return dirList


def analyseAllSimulations():
    setupNames = getListOfSimulationOutputs()

    for setupName in setupNames:
        print("Plotting", setupName)
        processSimulation(setupName)

    print("Done.")
    return
# %%
# analyseAllSimulations()
# %%
