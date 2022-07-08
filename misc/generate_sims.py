import os

sims = ["2j_2j_2s_3a_0pe",
        "2j_2j_2s_4a_0pe",
        "2j_2j_1s_3a_0pe",
        "2j_2j_1s_4a_0pe",
        "2j_3j_2.5s_4a_0pe",
        "3j_2j_2.5s_4a_0pe",
        "1j_1j_1s_2a_0pe",
        "1j_1j_1s_3a_0pe",
        "1j_1j_1s_4a_0pe",
        "1j_1j_2s_4a_0pe",
        "3j_3j_3s_2a_0pe",
        "3j_3j_3s_3a_0pe",
        "3j_3j_3s_4a_0pe",
        "3j_3j_5s_4a_0pe",
        "5j_5j_5s_2a_0pe",
        "5j_5j_5s_3a_0pe",
        "5j_5j_5s_4a_0pe",
        "8j_8j_8s_3a_0pe",
        "8j_8j_8s_4a_0pe",

        "1.33j_1j_1s_3a_0pe",
        "1j_1.33j_1s_3a_0pe",
        "0.7j_0.7j_0.7s_3a_0pe",
        "0.7j_0.7j_0.7s_4a_0pe",

        "1j_1.5j_1s_4a_0pe",
        "1.5j_1j_1s_4a_0pe",
        "4j_3j_3s_4a_0pe",
        "3j_6j_3s_4a_0pe",
        "5j_3j_4s_4a_0pe",
        "3j_5j_4s_4a_0pe",
        "6j_8j_7s_4a_0pe",
        "8j_6j_7s_4a_0pe",
        "7j_10j_8s_4a_0pe",
        "10j_10j_10s_3a_0pe",
        "10j_10j_10s_4a_0pe",
        ]

for sim in sims:
    os.system("python3 misc/new_sim.py %s" % sim)