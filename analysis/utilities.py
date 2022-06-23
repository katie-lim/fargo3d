# %%
import re
from typing import TypedDict
from operator import itemgetter
from glob import glob

class Simulation(TypedDict):
    m1: float
    m2: float
    sigma: float
    alpha: float
    photoevaporation: float


def getSimulationFromLabel(setupName) -> Simulation:
    regex = "([\d.]+j_[\d.]+j)_([\d.]+)s_(\d)a_([\d.]+)pe"
    matches = re.findall(regex, setupName)

    if len(matches) == 0:
        raise ValueError("The simulation label %s doesn't follow the convention." % setupName)

    planetNames, sigma, alpha, photoevaporation = matches[0]

    # [:-1] to ignore the j
    planetMasses = [float(planet[:-1]) for planet in planetNames.split("_")]
    m1, m2 = planetMasses

    spec: Simulation = {"m1": m1, "m2": m2, "sigma": sigma, "alpha": alpha, "photoevaporation": photoevaporation}

    return spec


def getParametersFromSimulation(sim: Simulation):
    m1, m2, sigma, alpha, photoevaporation = itemgetter("m1", "m2", "sigma", "alpha", "photoevaporation")(sim)

    return (m1, m2, sigma, alpha, photoevaporation)


def getParametersFromLabel(setupName: str):
    sim: Simulation = getSimulationFromLabel(setupName)

    return getParametersFromSimulation(sim)


def findLastOutputNumber(setupName):
    files = glob('outputs/%s/gasdens*.dat' % setupName)

    def extractNumber(f):
        s = re.findall("(\d+).dat$",f)
        return int(s[0]) if s else -1

    numbers = [extractNumber(file) for file in files]

    return max(numbers)
# %%
findLastOutputNumber("2-jupiter-2.5x-sigma0-0.001-alpha")
#%%
setupName = "2-jupiter-2.5x-sigma0-0.001-alpha"
files = glob('outputs/%s/gasdens*.dat' % setupName)