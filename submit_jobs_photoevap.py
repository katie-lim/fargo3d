# %%
import os
import re

def getFileContents(fileName):
    with open(fileName) as f:
        contents = f.read()

    return contents

def createJobScript(setupName):
    template = getFileContents("job_script_template_photoevap")

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
        "2j_2j_2s_4a_2pe",
        "3j_3j_3s_4a_3pe",
        "2j_2j_1s_4a_1pe",
        "1j_1j_1s_3a_1pe",
        "6j_8j_7s_4a_7pe",
        "3j_6j_3s_4a_3pe",
        "3j_5j_4s_4a_4pe",
        "5j_5j_5s_4a_5pe",
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
