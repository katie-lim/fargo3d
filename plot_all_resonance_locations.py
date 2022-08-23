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

        t = indexToRealTime(Nframes, parFile)
        title = "t = %.2f %s" % (t, unit_of_time)

        colors = ["#2ca02c", "#9467bd"]

        for i in [0, 1]:
            saveFileName = "analysis/plots/resonance_%d/resonance_%d_%s.png" % (i+1, i+1, setupName)
            planetFile = "outputs/%s/planet%d.dat" % (setupName, i)
            plotResonanceLocations(surfdens, velocity, parFile, planetFile, Nframes, i+1, color=colors[i], Nresonances=3, title=title, saveFileName=saveFileName)
            
    except Exception as e:
        print(e)
        print("Failed.")
        continue
