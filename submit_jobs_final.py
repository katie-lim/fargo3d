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

    jobIDs = re.findall("([0-9][0-9][0-9][0-9][0-9][0-9][0-9])", qstatOutput)
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
sims = [
#	"2j_2j_2s_4a_2pe",
#	"2j_2j_2s_4a_0pe",
#	"2j_2j_1s_4a_0pe",
#	"3j_3j_3s_4a_0pe",
#	"3j_3j_3s_4a_1pe",
#	"3j_3j_3s_4a_3pe",
#	"3j_3j_3s_4a_9pe",
#	"3j_5j_4s_4a_0pe",
#	"3j_5j_4s_4a_4pe",
#	"7j_10j_8s_4a_7.5R_0pe"

    "2j_2j_1s_4a_0pe",
    "2j_2j_1s_4a_1pe",
    "2j_2j_1s_4a_10pe",
    "2j_2j_2s_4a_0pe",
    "2j_2j_2s_4a_2pe",
    "2j_2j_2s_4a_20pe",
    "3j_3j_3s_4a_3pe",
    "3j_5j_4s_4a_0pe",
    "3j_5j_4s_4a_4pe",
    "3j_3j_3s_4a_0pe",
    "7j_10j_8s_4a_7.5R_0pe",
    "10j_10j_0.2667s_5a_6h_0pe",
    # "3j_3j_3s_4a_1pe",
    # "3j_3j_3s_4a_9pe",
    "3j_3j_3s_4a_30pe",
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
