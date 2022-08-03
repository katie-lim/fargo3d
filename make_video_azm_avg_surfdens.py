from analysis.plot import *
from analysis.utilities import *

import sys
# setupName = sys.argv[1]

setupName = "10j_10j_0.2667s_5a_6h_0pe"
Nframes = 657
# Nframes = 50

makeVideoAzmAvgSurfDens("video/%s/" % setupName, "video/%s.mp4" % setupName, "outputs/%s" % setupName, "setups/fargo/%s.par" % setupName, Nframes, True)
