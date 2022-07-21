# %%
from analysis.utilities import *
from analysis.plot import *
from os.path import exists
import os
import re


runningJobs = []
queuedJobs = []


def getRunningSims():
    qstatOutput = os.popen("qstat").read()
    jobIDs = re.findall("([0-9][0-9][0-9][0-9][0-9][0-9][0-9])", qstatOutput)

    for jobID in jobIDs:
        jobDetails = os.popen("qstat -f %s" % jobID).read()

        res = re.search("Job_Name = ([\S]+)", jobDetails)
        jobName = res.groups()[0]

        if jobName == "jupyterhub":
            continue

        res2 = re.search("job_state = ([\S]+)", jobDetails)
        state = res2.groups()[0]

        if state == "R":
            runningJobs.append(jobName)
        elif state == "Q":
            queuedJobs.append(jobName)

    return

getRunningSims()


def getPlotSavePath(plotName, setupName):
    return "analysis/plots/%s/%s_%s.png" % (plotName, plotName, setupName)


def getResultsTemplate():
    f = open("analysis/simulation_results_template.md", "r")
    template = f.read()
    f.close()

    return template


def plotResultsForSimulation(setupName, show=True):
    setupNameNoPe = getSetupNameNoPe(setupName)
    parFile = "setups/fargo/%s.par" % setupName

    orbit0 = "outputs/%s/orbit0.dat" % setupName
    orbit1 = "outputs/%s/orbit1.dat"% setupName
    files = [orbit0, orbit1]

    photoevap = not ("0pe" in setupName)

    lastOutputNumber = findLastOutputNumber(setupName)
    lastGasdens = "outputs/%s/gasdens%d.dat" % (setupName, lastOutputNumber)


    # Plot results
    if photoevap:
        plotOrbitalParameterPE(setupName, "semiMajorAxis", saveFileName=getPlotSavePath("semi_major_axes", setupName), show=show)
        plotOrbitalParameterPE(setupName, "eccentricity", saveFileName=getPlotSavePath("eccentricity", setupName), show=show)
    else:
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

    if photoevap:
        labels = ["no PE", "with PE"]
        lastOutputNumberInclPE = min(findLastOutputNumber(setupName), findLastOutputNumber(setupNameNoPe))
        time = indexToRealTime(lastOutputNumberInclPE, parFile)
        title = "%s with & without PE\nt = %.2f %s" % (setupNameNoPe.replace("_0pe", ""), time, unit_of_time)

        gasdensFiles = ["outputs/%s/gasdens%d.dat" % (s, lastOutputNumberInclPE) for s in [setupNameNoPe, setupName]]


        plotAzimuthallyAvgedSurfaceDensities(gasdensFiles, [parFile, parFile], True, logScale=True, saveFileName=getPlotSavePath("azimuthally_avged_surface_density", setupName), labels=labels, title=title, show=show)
    else:
        plotAzimuthallyAvgedSurfaceDensities([lastGasdens], [parFile], True, logScale=True, saveFileName=getPlotSavePath("azimuthally_avged_surface_density", setupName), show=show)

    return (periodRatio, stdDevPeriodRatio, suggestedResonance, orbit0, orbit1)


def writeSimulationResultsToFile(setupName, periodRatio, stdDevPeriodRatio, suggestedResonance, orbit0, orbit1):

    sim: Simulation = getSimulationFromLabel(setupName)
    simulationParams = list(sim.keys())
    simulationParamValues = list(sim.values())

    # Add other metadata
    status = "Not running"

    if (setupName in runningJobs):
        status = "Running"
    elif (setupName in queuedJobs):
        status = "Queuing"

    simulationParams.append("status")
    simulationParamValues.append(status)


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
        try:
            processSimulation(setupName)
        except Exception as e:
            print(e)

    print("Done.")
    return
# %%
# analyseAllSimulations()
# %%
