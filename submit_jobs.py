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
        # "6j_2j_1s_1a_7h_0pe",
        # "9j_3j_1s_1a_7h_0pe",
        # "6j_2j_0.2667s_5a_6h_0pe",
        # "9j_3j_0.2667s_5a_6h_0pe",
        # "6j_2j_0.667s_1a_9h_0pe",
        # "9j_3j_0.667s_1a_9h_0pe",
        # "6j_2j_1s_0.7a_8h_0pe",
        # "9j_3j_1s_0.7a_8h_0pe"


        # "3j_5j_0.2667s_5a_6h_1.375r_1.375r_0pe",
        # "2j_2j_0.2667s_5a_6h_1.375r_1.375r_0pe",
        # "10j_10j_0.2667s_5a_6h_1.375r_1.375r_0pe",
        # "2j_3j_0.2667s_5a_6h_1.375r_1.375r_0pe",
        # "3j_1j_0.667s_1a_9h_1.375r_1.375r_0pe",
        # "3j_1j_1s_1a_7h_1.375r_1.375r_0pe",
        # "1.33j_1j_0.2667s_5a_6h_1.375r_1.375r_0pe",
        # "5j_5j_0.2667s_5a_6h_1.375r_1.375r_0pe",
        # "5j_5j_1s_1a_7h_1.375r_1.375r_0pe",


        # "3j_1j_1s_1a_7h_0pe",
        # "10j_10j_1s_1a_7h_0pe",
        # "3j_1j_0.667s_1a_9h_0pe",
        # "10j_10j_0.667s_1a_9h_0pe",
        # "3j_1j_1s_0.7a_8h_0pe",
        # "10j_10j_1s_0.7a_8h_0pe",
        # "3j_1j_0.2667s_5a_6h_0pe",

#        "1j_1j_1s_1a_7h_0pe",
 #       "1.33j_1j_1s_1a_7h_0pe",
  #      "1j_1.33j_1s_1a_7h_0pe",
   #     "2j_2j_1s_1a_7h_0pe",
    #    "3j_3j_1s_1a_7h_0pe",
     #   "2j_3j_1s_1a_7h_0pe",
      #  "3j_2j_1s_1a_7h_0pe",
       # "5j_5j_1s_1a_7h_0pe",
#        "3j_5j_1s_1a_7h_0pe",
 #       "5j_3j_1s_1a_7h_0pe",
  #      "0.7j_0.7j_1s_1a_7h_0pe",


        # "1j_1j_0.2667s_5a_6h_0pe",
        # "1.33j_1j_0.2667s_5a_6h_0pe",
        # "1j_1.33j_0.2667s_5a_6h_0pe",
        # "2j_2j_0.2667s_5a_6h_0pe",
        # "3j_3j_0.2667s_5a_6h_0pe",
        # "2j_3j_0.2667s_5a_6h_0pe",
        # "3j_2j_0.2667s_5a_6h_0pe",
        # "5j_5j_0.2667s_5a_6h_0pe",
        # "3j_5j_0.2667s_5a_6h_0pe",
        # "5j_3j_0.2667s_5a_6h_0pe",
        # "0.7j_0.7j_0.2667s_5a_6h_0pe",


#        "1j_1j_0.667s_1a_9h_0pe",
 #       "1.33j_1j_0.667s_1a_9h_0pe",
  #      "1j_1.33j_0.667s_1a_9h_0pe",
   #     "2j_2j_0.667s_1a_9h_0pe",
    #    "3j_3j_0.667s_1a_9h_0pe",
     #   "2j_3j_0.667s_1a_9h_0pe",
      #  "3j_2j_0.667s_1a_9h_0pe",
       # "5j_5j_0.667s_1a_9h_0pe",
#        "3j_5j_0.667s_1a_9h_0pe",
 #       "5j_3j_0.667s_1a_9h_0pe",
  #      "0.7j_0.7j_0.667s_1a_9h_0pe",

#        "1j_1j_1s_0.7a_8h_0pe",
 #       "1.33j_1j_1s_0.7a_8h_0pe",
  #      "1j_1.33j_1s_0.7a_8h_0pe",
   #     "2j_2j_1s_0.7a_8h_0pe",
    #    "3j_3j_1s_0.7a_8h_0pe",
     #   "2j_3j_1s_0.7a_8h_0pe",
      #  "3j_2j_1s_0.7a_8h_0pe",
       # "5j_5j_1s_0.7a_8h_0pe",
#        "3j_5j_1s_0.7a_8h_0pe",
 #       "5j_3j_1s_0.7a_8h_0pe",
  #      "0.7j_0.7j_1s_0.7a_8h_0pe",



        # "3j_1j_1s_1a_7h_1.375r_1.375r_0pe",
	    # "7j_7j_0.2667s_5a_6h_0pe",
        # "7j_7j_0.667s_1a_9h_0pe",
        # "7j_7j_1s_1a_7h_0pe",
        # "7j_7j_1s_0.7a_8h_0pe",
        # "10j_10j_0.2667s_5a_6h_0pe",
        # "5j_5j_0.2667s_5a_6h_0pe",


        # "5j_3j_0.667s_1a_9h_0pe",
#        "9j_3j_0.667s_1a_9h_0pe",
 #       "3j_3j_1s_1a_7h_0pe",



        # New simulations
        # "4.5j_2j_0.2667s_5a_6h_0pe",
        # "4.5j_2j_1s_0.7a_8h_0pe",

        # "5j_5j_0.667s_1a_9h_1.5r_1.5r_4.5R_0pe",
        # "5j_5j_1s_0.7a_8h_1.5r_1.5r_4.5R_0pe",
        # "5j_5j_1s_1a_7h_1.5r_1.5r_4.5R_0pe",
        # "2j_2j_0.2667s_5a_6h_1.5r_1.5r_4.5R_0pe",
        # "2j_2j_0.667s_1a_9h_1.5r_1.5r_4.5R_0pe",
        # "2j_3j_0.2667s_5a_6h_1.5r_1.5r_4.5R_0pe",
        # "3j_1j_1s_1a_7h_1.5r_1.5r_4.5R_0pe",
        # "1j_1j_1s_1a_7h_1.5r_1.5r_4.5R_0pe",
        # "3j_5j_0.667s_1a_9h_1.5r_1.5r_4.5R_0pe",
        # "1j_1j_0.667s_1a_9h_1.5r_1.5r_4.5R_0pe",
        # "1j_1j_0.2667s_5a_6h_1.5r_1.5r_4.5R_0pe",


        # "5j_5j_0.667s_1a_9h_1.5r_1.5r_4.5R_0pe_f",
        # "5j_5j_1s_0.7a_8h_1.5r_1.5r_4.5R_0pe_f",
        # "5j_5j_1s_1a_7h_1.5r_1.5r_4.5R_0pe_f",
        # "2j_2j_0.2667s_5a_6h_1.5r_1.5r_4.5R_0pe_f",
        # "2j_2j_0.667s_1a_9h_1.5r_1.5r_4.5R_0pe_f",
        # "2j_3j_0.2667s_5a_6h_1.5r_1.5r_4.5R_0pe_f",
        # "3j_1j_1s_1a_7h_1.5r_1.5r_4.5R_0pe_f",
        # "1j_1j_1s_1a_7h_1.5r_1.5r_4.5R_0pe_f",
        # "3j_5j_0.667s_1a_9h_1.5r_1.5r_4.5R_0pe_f",
        # "1j_1j_0.667s_1a_9h_1.5r_1.5r_4.5R_0pe_f",
        # "1j_1j_0.2667s_5a_6h_1.5r_1.5r_4.5R_0pe_f",


        # "5j_5j_0.2667s_5a_6h_1.5r_1.5r_4.5R_0pe",
        # "5j_5j_0.2667s_5a_6h_1.5r_1.5r_4.5R_0pe_f",
        # "7j_5j_1s_1a_7h_1.5r_1.5r_4.5R_0pe",
        # "3j_2j_0.2667s_5a_6h_0pe_f",
        # "3j_3j_0.667s_1a_9h_0pe_f",
        # "3j_3j_0.2667s_5a_6h_0pe_f",
        # "3j_3j_1s_1a_7h_0pe_f",
        # "4j_3j_0.667s_1a_9h_0pe",
        # "4j_3j_0.2667s_5a_6h_0pe",
        # "4j_3j_1s_1a_7h_0pe",
        # "4j_3j_0.667s_1a_9h_1.5r_1.5r_4.5R_0pe",
        # "4j_3j_0.2667s_5a_6h_1.5r_1.5r_4.5R_0pe",
        # "4j_3j_1s_1a_7h_1.5r_1.5r_4.5R_0pe"

        "4j_3j_1s_0.7a_8h_0pe",
        "4j_3j_1s_0.7a_8h_1.5r_1.5r_4.5R_0pe",
        "4j_2j_0.667s_1a_9h_0pe",
        "4j_2j_0.2667s_5a_6h_0pe",
        "4j_2j_1s_1a_7h_0pe",
        "4j_2j_1s_0.7a_8h_0pe",
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
