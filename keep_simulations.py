from analysis.plot_results import getListOfSimulationOutputs
import os

setupsToKeep = [
    "7j_7j_1s_0.7a_8h_1pe",
    "7j_7j_1s_1a_7h_0pe",
    "7j_7j_1s_1a_7h_1pe",
    "10j_10j_0.2667s_5a_6h_0pe",
    "10j_10j_0.2667s_5a_6h_0.2667pe",
    "3j_1j_1s_1a_7h_0pe",
    "3j_1j_1s_1a_7h_1pe",
    "7j_7j_0.667s_1a_9h_0pe",
    "7j_7j_0.667s_1a_9h_0.667pe",
    "7j_7j_1s_1a_7h_0pe",
    "7j_7j_1s_1a_7h_1pe"
]

setupsToMove = []
setupNames = getListOfSimulationOutputs()

for setupName in setupNames:
    if not (setupName in setupsToKeep):
        setupsToMove.append(setupName)

print(setupsToMove)
ans = input("Remove these files? (Y/N): ")

if ans.upper() == "Y":
    os.system("mkdir outputs/outputs_to_move")

    for setupName in setupsToMove:
        print(setupName)
        os.system("mv outputs/%s outputs/outputs_to_move" % (setupName))
