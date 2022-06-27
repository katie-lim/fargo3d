# %%
import os
import re

def getFileContents(fileName):
    with open(fileName) as f:
        contents = f.read()

    return contents

def createJobScript(setupName):
    template = getFileContents("job_script_template")

    script = template.replace("{{SETUPNAME}}", setupName)

    with open(setupName, "w") as f:
        f.write(script)

    return

def getRunningSims():
    qstatOutput = os.popen("qstat").read()

    jobIDs = re.findall("([0-9]+).pbs", qstatOutput)
    jobs = []

    for jobID in jobIDs:
        jobDetails = os.popen("qstat -f %s" % jobID).read()

        res = re.search("Job_Name = ([\S]+)", jobDetails)
        jobName = res.groups()[0]

        jobs.append(jobName)

    # Remove "jupyterhub" job
    try:
        jobs.remove("jupyterhub")
    except:
        pass

    return jobs


simsToSubmit = []
sims = ["2j_2j_2s_3a_0pe",
        "2j_2j_2s_4a_0pe",
        "2j_2j_1s_4a_0pe",
        "1j_1j_1s_3a_0pe",
        "1j_1j_1s_4a_0pe",
        "1j_1j_2s_4a_0pe",
        "3j_3j_3s_3a_0pe",
        "3j_3j_3s_4a_0pe",
        "5j_5j_5s_3a_0pe",
        "5j_5j_5s_4a_0pe",
        "8j_8j_8s_3a_0pe",
        "8j_8j_8s_4a_0pe",

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

runningSims = getRunningSims()

# Ignore simulations already running
for sim in sims:
    if not (sim in runningSims):
        simsToSubmit.append(sim)

print("Submitting simulations:", simsToSubmit)
ans = input("Continue? (Y/N):")

if ans.capitalize() == "Y":
    for sim in simsToSubmit:
        createJobScript(sim)
        os.system("qsub %s" % sim)

# %%
