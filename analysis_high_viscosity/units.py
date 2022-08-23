import numpy as np

dpi = 200

# Units
au = 1.496e11 # m
R0 = 20
R0_unit = "AU"
R0_in_m = 20*au
Mstar = 1
Mstar_unit = "M_Sun"
Mstar_in_kg = 1.989e30
density_scale_factor = (Mstar_in_kg / R0_in_m**2) / 10
density_unit = "gcm$^{-2}$"

unit_of_time_in_s = 3.154e7 # seconds in a year
unit_of_time = "yr"



def calcOrbitalPeriodInRealUnits(semiMajorAxisInM=1.496e11):
    """Returns the orbital period in real units of a planet orbiting the central star with the specified semi-major axis.

    Args:
        semiMajorAxisInM (float): The planet's semi-major axis in metres.

    Returns:
        orbitalPeriod (float): The planet's orbital period in the user-defined time unit.
    """
    orbitalPeriod = 2*np.pi * np.sqrt((semiMajorAxisInM)**3 / (6.67e-11 * Mstar_in_kg)) # calculate the orbital period in seconds using Kepler's 3rd law
    orbitalPeriod /= unit_of_time_in_s    # convert to the chosen time unit

    return orbitalPeriod


def convertToRealTime(t):
    """Converts a given time in scale-free units to real units.

    Args:
        t (float): A time in scale free-units.
    Returns:
        The time in real units.
    """

    return t/(2*np.pi) * calcOrbitalPeriodInRealUnits(R0_in_m)