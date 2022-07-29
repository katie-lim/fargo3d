import math
import sys
from shutil import copyfile
import re

from numpy import outer

setupName = sys.argv[1]


def extractPlanetRadii(N, planetRadiiMultipliers):

    # By default, start the 1st planet at r=1,
    # the 2nd at r=2, and the 3rd at r=3, etc

    if planetRadiiMultipliers != "":
        planet_radii_multipliers = [float(planet[:-1]) for planet in planetRadiiMultipliers.split("_")[:-1]]
    else:
        planet_radii_multipliers = [1 for i in range(N)]

    planet_radii = [(i+1)*planet_radii_multipliers[i] for i in range(N)]

    return planet_radii



def generate_planet_cfg(planetNames, planetRadiiMultipliers):
    planet_mass_multipliers = [float(planet[:-1]) for planet in planetNames.split("_")]

    planet_masses = [0.001 * pm for pm in planet_mass_multipliers]

    planet_radii = extractPlanetRadii(len(planet_masses), planetRadiiMultipliers)

    # Generate the .cfg file
    if planetRadiiMultipliers == "":
        fileName = "planets/%s.cfg" % planetNames
    else:
        fileName = "planets/%s_%s.cfg" % (planetNames, planetRadiiMultipliers[:-1]) # :-1 to exclude the _

    copyfile("planets/planet_template.cfg", fileName)

    with open(fileName, "a") as f:
        for i in range(len(planet_masses)):
            f.write("\nJupiter%d	 	%.3f		%.6f	 0.0		YES   		YES" % (i+1, planet_radii[i], planet_masses[i]))


    # Generate the .cfg file with fixed planets (set 'Feels disk' and 'Feels others' to NO)
    if planetRadiiMultipliers == "":
        fileName = "planets/fixed/%s_fixed.cfg" % planetNames
    else:
        fileName = "planets/fixed/%s_%s_fixed.cfg" % (planetNames, planetRadiiMultipliers[:-1]) # :-1 to exclude the _

    copyfile("planets/planet_template.cfg", fileName)

    with open(fileName, "a") as f:
        for i in range(len(planet_masses)):
            f.write("\nJupiter%d	 	%.3f		%.6f	 0.0		NO   		NO" % (i+1, planet_radii[i], planet_masses[i]))



    # Generate a .cfg file with the inner planet fixed
    if planetRadiiMultipliers == "":
        fileName = "planets/inner_fixed/%s_inner_fixed.cfg" % planetNames
    else:
        fileName = "planets/inner_fixed/%s_%s_inner_fixed.cfg" % (planetNames, planetRadiiMultipliers[:-1]) # :-1 to exclude the _

    copyfile("planets/planet_template.cfg", fileName)

    with open(fileName, "a") as f:
        for i in range(len(planet_masses)):
            if i == 0:
                f.write("\nJupiter%d	 	%.3f		%.6f	 0.0		NO   		NO" % (i+1, planet_radii[i], planet_masses[i]))
            else:
                f.write("\nJupiter%d	 	%.3f		%.6f	 0.0		YES   		YES" % (i+1, planet_radii[i], planet_masses[i]))




def generate_par_file(setupName):
    regex = "([\d.]+j_[\d.]+j)_([\d.]+)s_([\d.]+)a_([\d.]+)h_([\d.]+r_[\d.]+r_)?([\d.]+R_)?([\d.]+)pe(_f)?"
    matches = re.findall(regex, setupName)
    print(matches[0])

    if len(matches) > 0:
        planetNames, surfaceDensity, alpha, aspectRatio, planetRadii, outerBound, photoevaporation, innerFixed = matches[0]


        if innerFixed == "_f":
            if planetRadii == "":
                planet_cfg = "planets/inner_fixed/%s_inner_fixed.cfg" % planetNames
                planet_cfg_fixed = "planets/inner_fixed/%s_inner_fixed.cfg" % planetNames
            else:
                planet_cfg = "planets/inner_fixed/%s_%s_inner_fixed.cfg" % (planetNames, planetRadii[:-1])
                planet_cfg_fixed = "planets/inner_fixed/%s_%s_inner_fixed.cfg" % (planetNames, planetRadii[:-1])
        else:
            if planetRadii == "":
                planet_cfg = "planets/%s.cfg" % planetNames
                planet_cfg_fixed = "planets/fixed/%s_fixed.cfg" % planetNames
            else:
                planet_cfg = "planets/%s_%s.cfg" % (planetNames, planetRadii[:-1])
                planet_cfg_fixed = "planets/fixed/%s_%s_fixed.cfg" % (planetNames, planetRadii[:-1])

        alpha = float(alpha) * 1e-3
        surf_dens = float(surfaceDensity)
        aspect_ratio = float(aspectRatio) * 0.01
        pe = float(photoevaporation)

        # Generate the planet .cfg files
        generate_planet_cfg(planetNames, planetRadii)


        # Compute the inner planet's orbital radius
        # So we can adjust MassTaper and FixedNtot to be 100 and 200 initial inner orbits
        N = len(planetNames.split("_"))
        planetRadii = extractPlanetRadii(N, planetRadii)
        innerPlanetRadius = planetRadii[0]

        # P² ∝ a³
        dt = 0.314159265359
        orbits100 = 628.3185 * math.pow(innerPlanetRadius, 3/2)
        orbits200 = 2 * orbits100


        # Set the default outer boundary
        if (outerBound == ""):
            outerBound = 3.75
        else:
            outerBound = outerBound[:-2] # Remove the "R_"
            outerBound = float(outerBound)


        # Create the .par files for the simulation
        f1 = open('setups/fargo/template.par', 'r')
        f2 = open("setups/fargo/%s.par" % setupName, 'w')

        if innerFixed != "_f":
            f3 = open("setups/fargo/fixed/%s_fixed.par" % setupName, 'w')

        placeholders = ("{{SIGMA0}}", "{{ALPHA}}", "{{ASPECTRATIO}}", "{{PHOTOEVAPORATION}}", "{{PLANET_CFG}}", "{{OUTPUT}}", "{{MASSTAPER}}", "{{FIXEDNTOT}}", "{{OUTERBOUNDARY}}")
        replace = (
                    "%.10e" % (3.3755897436e-03 * surf_dens),
                    "%.3e" % (alpha),
                    "%.3f" % (aspect_ratio),
                    "%.2e" % (1.0e43 * (pe**2)),
                    planet_cfg,
                    setupName,
                    "%.4f" % (orbits100),
                    "%d" % (round(orbits200 / dt)),
                    "%.2f" % (outerBound)
        )

        for line in f1:
            for placeholder, rep in zip(placeholders, replace):
                line = line.replace(placeholder, rep)
            f2.write(line)

            if innerFixed != "_f":
                if line.startswith("PlanetConfig"):
                    line = line.replace(planet_cfg, planet_cfg_fixed)
                elif line.startswith("FixedNtot"):
                    line = line.replace("FixedNtot", "Ntot")
                elif line.startswith("Ntot"):
                    line = line.replace("Ntot", "TotalNtot")

                f3.write(line) 

        f1.close()
        f2.close()

        if innerFixed != "_f":
            f3.close()

    else:
        print("The simulation label %s doesn't follow convention." % setupName)


generate_par_file(setupName)