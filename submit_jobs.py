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

    jobs = re.findall("[0-9]+.pbs[\s]+([\S]+)", qstatOutput)

    # Remove "jupyterhub" job
    jobs.remove("jupyterhub")

    return jobs


sims = ["2j_2j_2s_4a_0pe",
        "1j_1j_1s_3a_0pe",
        "1j_1j_1s_4a_0pe",
        "3j_3j_5s_4a_0pe",
        "5j_5j_5s_4a_0pe",
        ]

runningSims = getRunningSims()

for sim in sims:
    # Ignore currently running jobs
    if (sim in runningSims):
        # print("%s is already running." % sim)
        continue

    createJobScript(sim)
    os.system("qsub %s" % sim)

# %%
