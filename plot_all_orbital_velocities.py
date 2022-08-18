from analysis.plot import *
from analysis.utilities import *
from analysis.plot_results import getListOfSimulationOutputs

for setupName in getListOfSimulationOutputs():
    print(setupName)
    try:
        Nframes = findLastOutputNumber(setupName)

        velocity = "outputs/%s/gasvx%d.dat" % (setupName, Nframes)
        surfdens = "outputs/%s/gasdens%d.dat" % (setupName, Nframes)
        parFile = "setups/fargo/%s.par" % (setupName)
        saveFileName = "analysis/plots/angular_velocity/angular_velocity_%s.png" % (setupName)

        plotAzimuthallyAvgedOrbitalVel([velocity], [surfdens], [parFile], logRadialSpacing=True, massWeighted=True, angularVelocity=True, title=velocity, saveFileName=saveFileName)

    except:
        print("Failed.")
        continue
