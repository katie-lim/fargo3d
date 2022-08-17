from analysis.plot import *
from analysis.utilities import *
from os import path

setupNames = [
        "1.33j_1j_0.667s_1a_9h_0pe",
        "1j_1j_0.2667s_5a_6h_0pe",
        "1j_1j_1s_1a_7h_1.5r_1.5r_4.5R_0pe",
        "3j_1j_1s_0.7a_8h_0pe",
        "2j_2j_1s_1a_7h_0pe",
        "3j_5j_0.667s_1a_9h_1.5r_1.5r_4.5R_0pe_f",
        "5j_5j_0.667s_1a_9h_0pe",
        "5j_5j_1s_0.7a_8h_1.5r_1.5r_4.5R_0pe",
        "5j_5j_1s_1a_7h_0pe",
        "7j_7j_1s_0.7a_8h_0pe"
    ]

for setupName in setupNames:
    # Check folder exists
    if path.exists("outputs/%s" % setupName):
        print("Making video for %s." % setupName)

        Nframes = findLastOutputNumber(setupName)

        makeVideo("video/%s/" % setupName, "video/%s.mp4" % setupName, "outputs/%s" % setupName, "setups/fargo/%s.par" % setupName, "gasdens", Nframes, True)
    else:
        print("Simulation %s is not stored here." % setupName)