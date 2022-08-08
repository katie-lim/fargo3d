from analysis.plot import *
from analysis.utilities import *

import sys
# setupName = sys.argv[1]

setupName = "1j_1j_0.2667s_5a_6h_1.5r_1.5r_4.5R_0pe_f"
Nframes = 438
# Nframes = 50

makeVideoAzmAvgSurfDens("video/%s/" % setupName, "video/%s.mp4" % setupName, "outputs/%s" % setupName, "setups/fargo/%s.par" % setupName, Nframes, True, vmax=5)
