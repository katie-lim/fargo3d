# %%
from analysis.plot import *
from analysis.utilities import *

# import sys
# setupName = sys.argv[1]

setupName = "10j_10j_0.2667s_5a_6h_0.2667pe"
Nframes = findLastOutputNumber(setupName)

plotOrbitalParameterPE(setupName, "eccentricity")

# %%