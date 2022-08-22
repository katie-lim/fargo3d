# %%
from operator import index
from analysis.plot import *
from analysis.utilities import *

# import sys
# setupName = sys.argv[1]

setupName = "7j_7j_0.667s_1a_9h_0pe"
Nframes = findLastOutputNumber(setupName)

velocity = "outputs/%s/gasvx%d.dat" % (setupName, Nframes)
surfdens = "outputs/%s/gasdens%d.dat" % (setupName, Nframes)
parFile = "setups/fargo/%s.par" % (setupName)
saveFileName = "analysis/plots/angular_velocity/angular_velocity_%s.png" % (setupName)

t = indexToRealTime(Nframes, parFile)
title = "t = %.2f %s" % (t, unit_of_time)

colors = ["#2ca02c", "#9467bd"]

for i in [0, 1]:
    planetFile = "outputs/%s/planet%d.dat" % (setupName, i)
    plotResonanceLocations(surfdens, velocity, parFile, planetFile, Nframes, i+1, color=colors[i], Nresonances=3, title=title)

# %%