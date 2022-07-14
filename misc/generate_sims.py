import os

sims = [
        "1j_1j_1s_1a_0pe",
        "1.33j_1j_1s_1a_0pe",
        "1j_1.33j_1s_1a_0pe",
        "2j_2j_1s_1a_0pe",
        "3j_3j_1s_1a_0pe",
        "2j_3j_1s_1a_0pe",
        "3j_2j_1s_1a_0pe",
        "5j_5j_1s_1a_0pe",
        "3j_5j_1s_1a_0pe",
        "5j_3j_1s_1a_0pe",
        "0.7j_0.7j_1s_1a_0pe",
        ]

for sim in sims:
    os.system("python3 misc/new_sim.py %s" % sim)