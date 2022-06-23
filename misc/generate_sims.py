import os

sims = [
    "1.33j_1.33j_1s_3a_0pe",
    "1.33j_1.33j_1.5s_3a_0pe",
    "1.33j_1.33j_2s_4a_0pe",
    "1.33j_1.33j_4s_4a_0pe",
    "1.33j_1j_1s_4a_0pe",
    "1.33j_1j_2s_4a_0pe",
    "1.33j_1j_4s_4a_0pe",
    "1.75j_1.75j_1s_4a_0pe",
    "1j_1j_1s_3a_0pe",
    "1j_1j_0.6s_3a_0pe",
    "1j_1j_0.6s_4a_0pe",
    "1j_1j_1.5s_3a_0pe",
    "1j_1j_1.5s_4a_0pe",
    "1j_1j_1s_4a_0pe",
    "1j_1j_2.5s_3a_0pe",
    "1j_1j_2s_3a_0pe",
    "1j_1j_2s_4a_0pe",
    "1j_1j_3s_4a_0pe",
    "1j_1j_4s_4a_0pe",
    "2j_2j_1s_3a_0pe",
    "2j_2j_1s_4a_0pe",
    "2j_2j_1s_5a_0pe",
    "2j_2j_2s_4a_0pe",
    "2j_2j_3s_4a_0pe",
    "2j_2j_4s_4a_0pe",
    "2j_2j_5s_4a_0pe",
    "2j_3j_1s_4a_0pe",
    "2j_4j_5s_4a_0pe",
    "2j_1j_1s_4a_0pe",
    "3j_2j_1s_4a_0pe",
    "3j_3j_1s_3a_0pe",
    "3j_3j_1s_4a_0pe",
    "3j_3j_2s_4a_0pe",
    "3j_3j_5s_4a_0pe",
    "3j_6j_2.5s_4a_0pe",
    "4j_2j_1.5s_4a_0pe",
    "4j_3j_3s_4a_0pe",
    "4j_4j_1s_3a_0pe",
    "5j_5j_2.5s_4a_0pe",
    "5j_5j_5s_4a_0pe",
    "5j_10j_5s_4a_0pe",
    "6j_3j_2.5s_4a_0pe",
    "6j_6j_3s_4a_0pe",
    "7j_10j_5s_4a_0pe",
    "8j_6j_5s_4a_0pe",
    "8j_8j_5s_4a_0pe",
    "10j_10j_5s_4a_0pe",
    "10j_10j_10s_4a_0pe"
]

for sim in sims:
    os.system("python3 misc/new_sim.py %s" % sim)