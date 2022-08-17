# %%
from analysis.plot import *
from analysis.utilities import *

import sys
setupName = sys.argv[1]

setupName = "10j_10j_0.2667s_5a_6h_0pe"

Nframes = findLastOutputNumber(setupName)
# Nframes = 0

velocity = "outputs/%s/gasvx%d.dat" % (setupName, Nframes)
surfdens = "outputs/%s/gasdens%d.dat" % (setupName, Nframes)
parFile = "setups/fargo/%s.par" % (setupName)


plotAzimuthallyAvgedOrbitalVel([velocity], [surfdens], [parFile], logRadialSpacing=True, massWeighted=True, title=velocity)
plotAzimuthallyAvgedOrbitalVel([velocity], [surfdens], [parFile], logRadialSpacing=True, massWeighted=True, angularVelocity=True, title=velocity)
# %%