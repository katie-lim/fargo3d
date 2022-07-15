import sys
from shutil import copyfile
import re

setupName = sys.argv[1]

def generate_planet_cfg(planetNames):
    planet_mass_multipliers = [float(planet[:-1]) for planet in planetNames.split("_")]

    planet_masses = [0.001 * pm for pm in planet_mass_multipliers]

    # Generate the .cfg file
    fileName = ("planets/%s.cfg" % planetNames)
    copyfile("planets/planet_template.cfg", fileName)

    with open(fileName, "a") as f:
        # By default, start the 1st planet at r=1,
        # the 2nd at r=2, and the 3rd at r=3, etc

        for i in range(len(planet_masses)):
            f.write("\nJupiter%d	 	%.2f		%s	 0.0		YES   		YES" % (i+1, float(i+1), planet_masses[i]))


    # Generate the .cfg file with fixed planets (set 'Feels disk' and 'Feels others' to NO)
    fileName = ("planets/fixed/%s_fixed.cfg" % planetNames)
    copyfile("planets/planet_template.cfg", fileName)

    with open(fileName, "a") as f:
        for i in range(len(planet_masses)):
            f.write("\nJupiter%d	 	%.2f		%s	 0.0		NO   		NO" % (i+1, float(i+1), planet_masses[i]))



def generate_par_file(setupName):
    regex = "([\d.]+j_[\d.]+j)_([\d.]+)s_([\d.]+)a_([\d.]+)h_([\d.]+)pe"
    matches = re.findall(regex, setupName)
    print(matches[0])

    if len(matches) > 0:
        planetNames, surfaceDensity, alpha, aspectRatio, photoevaporation = matches[0]

        planet_cfg = "planets/%s.cfg" % planetNames
        planet_cfg_fixed = "planets/fixed/%s_fixed.cfg" % planetNames
        alpha = float(alpha) * 1e-3
        surf_dens = float(surfaceDensity)
        aspect_ratio = float(aspectRatio) * 0.01
        pe = float(photoevaporation)

        # Generate the planet .cfg files
        generate_planet_cfg(planetNames)


        # Create the .par files for the simulation
        f1 = open('setups/fargo/template.par', 'r')
        f2 = open("setups/fargo/%s.par" % setupName, 'w')
        f3 = open("setups/fargo/fixed/%s_fixed.par" % setupName, 'w')

        placeholders = ("{{SIGMA0}}", "{{ALPHA}}", "{{ASPECTRATIO}}", "{{PHOTOEVAPORATION}}", "{{PLANET_CFG}}", "{{OUTPUT}}")
        replace = ("%.10e" % (3.3755897436e-03 * surf_dens),
                    "%.3e" % (alpha),
                    "%.3f" % (aspect_ratio),
                    "%.2e" % (1.0e43 * (pe**2)),
                    planet_cfg,
                    setupName)

        for line in f1:
            for placeholder, rep in zip(placeholders, replace):
                line = line.replace(placeholder, rep)
            f2.write(line)


            if (line[:12] == "PlanetConfig"):
                line = line.replace(planet_cfg, planet_cfg_fixed)
            elif (line[:9] == "FixedNtot"):
                line = line.replace("FixedNtot", "Ntot")
            elif (line[:4] == "Ntot"):
                line = line.replace("Ntot", "TotalNtot")

            f3.write(line)

        f1.close()
        f2.close()
        f3.close()

    else:
        print("The simulation label %s doesn't follow convention." % setupName)


generate_par_file(setupName)