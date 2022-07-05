# %%
import re
import os
import shutil
import sys
sys.path.insert(0, os.path.abspath('./'))
import analysis.units

Ninterm = 200


sims = [
    ("2j_2j_2s_4a_1pe", 60000),
    ("3j_3j_3s_4a_3pe", 50000),
    ("2j_2j_1s_4a_1pe", 100000),

    ("1j_1j_1s_3a_1pe", 100000),
    ("6j_8j_7s_4a_7pe", 50000),
    ("3j_6j_3s_4a_3pe", 100000),
    ("3j_5j_4s_4a_4pe", 80000),
    ("5j_5j_5s_4a_4pe", 50000),
]


conversionFactor = analysis.units.convertToRealTime(1)

for (setupName, photoevapStartTime) in sims:
    print("%s" % setupName)
    setupNameNoPe = re.sub("[0-9]pe", "0pe", setupName)


    # Calculate output number to start PE at
    print("Start photoevaporation after %d years" % photoevapStartTime)

    photoevapCodeUnits = (photoevapStartTime / conversionFactor)
    DTs = photoevapCodeUnits / 0.314159265359
    outputs = DTs / Ninterm
    outputNo = round(outputs)

    print("= %.3f in code units" % photoevapCodeUnits)
    print("= %.3f DTs" % DTs)
    print("= %.3f scalar field outputs" % outputs)
    print("=> Output #%d" % outputNo)


    # Copy over result files with no PE
    outputFileNames = ["gasdens", "gasenergy", "gasvx", "gasvy", "summary"]
    outputFiles = ["%s%d" % (fileName, outputNo) for fileName in outputFileNames]
    orbitFiles = ["orbit%d" % i for i in [0, 1]]


    files = outputFiles + orbitFiles
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
    os.system("python misc/new_sim.py %s" % setupName)
    print("")

# %%