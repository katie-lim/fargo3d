from analysis.plot import *
from analysis.utilities import *

import sys
setupName = sys.argv[1]

#setupName = "1j_1j_1s_1a_7h_1.5r_1.5r_4.5R_0pe"
Nframes = findLastOutputNumber(setupName)

makeVideo("video/%s/" % setupName, "video/%s.mp4" % setupName, "outputs/%s" % setupName, "setups/fargo/%s.par" % setupName, "gasdens", Nframes, True)
