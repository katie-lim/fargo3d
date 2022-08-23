# %%
import os
import shutil
import sys
sys.path.insert(0, os.path.abspath('./'))
import analysis.units
from analysis.utilities import *

dt = 0.314159265359
Ninterm = 200
conversionFactor = analysis.units.convertToRealTime(1)


sims = [
    # ("7j_7j_0.667s_1a_9h_0.667pe", 125000),
    # ("7j_7j_1s_1a_7h_1pe", 150000),
#    ("10j_10j_0.2667s_5a_6h_0.2667pe", 175000),
    # ("7j_7j_0.2667s_5a_6h_0.2667pe", 275000),
    # ("7j_7j_1s_0.7a_8h_1pe", 500000),
    # ("3j_1j_1s_1a_7h_1pe", 500000),
    # ("5j_5j_1s_1a_7h_1.5r_1.5r_4.5R_1pe", 100000),
    # ("5j_5j_0.2667s_5a_6h_1pe", 100000)

    ("2j_2j_1s_4a_1pe", 100000),
    ("2j_2j_1s_4a_10pe", 100000),
    ("2j_2j_2s_4a_2pe", 75000),
    ("2j_2j_2s_4a_20pe", 75000),
    # ("3j_3j_3s_4a_1pe", 50000),
    # ("3j_3j_3s_4a_3pe", 50000),
    # ("3j_3j_3s_4a_9pe", 50000),
    # ("3j_3j_3s_4a_6pe", 50000),
    # ("2j_2j_1s_4a_1pe", 100000),

    # ("1j_1j_1s_3a_1pe", 100000),
    # ("6j_8j_7s_4a_7pe", 50000),
    # ("3j_6j_3s_4a_3pe", 100000),
    # ("3j_5j_4s_4a_4pe", 80000),
    # ("5j_5j_5s_4a_5pe", 50000),
    # ("7j_10j_8s_4a_8pe", 150000)
]


for (setupName, photoevapStartTime) in sims:
    print(setupName)
    setupNameNoPe = getSetupNameNoPe(setupName)


    # Calculate output number to start PE at
    print("Start photoevaporation after %d years" % photoevapStartTime)

    photoevapCodeUnits = (photoevapStartTime / conversionFactor)
    DTs = photoevapCodeUnits / dt
    outputs = DTs / Ninterm
    outputNo = round(outputs)

    print("= %.3f in code units" % photoevapCodeUnits)
    print("= %.3f DTs" % DTs)
    print("= %.3f scalar field outputs" % outputs)
    print("=> Output #%d" % outputNo)


    # Copy over result files with no PE
    outputFileNames = ["gasdens", "gasenergy", "gasvx", "gasvy", "summary"]
    outputFiles = ["%s%d" % (fileName, outputNo) for fileName in outputFileNames]
    planetFiles = ["planet%d" % i for i in [0, 1]]


    files = outputFiles + planetFiles
    for file in files:

        src = "outputs/%s/%s.dat" % (setupNameNoPe, file)
        dstFolder = "outputs/%s/" % setupName
        dst = "outputs/%s/%s.dat" % (setupName, file)

        try:
            os.makedirs(dstFolder, exist_ok=True)
            shutil.copy(src, dst)
        except Exception as e:
            print("Failed to copy %s to %s. Error:" % (src, dst))
            print(e)


    # Generate .par files for the new simulation with PE
    # os.system("python misc/new_sim.py %s" % setupName)
    print("")

# %%
