import sys
import re

setupName = sys.argv[1]

regex = "([\d.]+j_[\d.]+j)_([\d.]+)s_(\d)a_([\d.]+)pe"
matches = re.findall(regex, setupName)
print(matches[0])

if len(matches) > 0:
    planet_cfg, surface_density, alpha, photoevaporation = matches[0]

    surf_dens = float(surface_density)
    pe = float(photoevaporation)


    # Create the .par file for the simulation
    f1 = open('setups/fargo/template.par', 'r')
    f2 = open("setups/fargo/%s.par" % setupName, 'w')

    placeholders = ("{{SIGMA0}}", "{{ALPHA}}", "{{PHOTOEVAPORATION}}", "{{PLANET_CFG}}", "{{OUTPUT}}")
    replace = ("%.10e" % (6.3661977237e-4 * surf_dens), alpha, "%.2e" % (4.0e43 * (pe**2)), planet_cfg, setupName)

    for line in f1:
        for placeholder, rep in zip(placeholders, replace):
            line = line.replace(placeholder, rep)
        f2.write(line)

    f1.close()
    f2.close()
else:
    print("The simulation label %s doesn't follow convention." % setupName)