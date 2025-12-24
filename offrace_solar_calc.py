import numpy as np
from scipy.integrate import quad
from race_config import PanelArea, PanelEfficiency, RaceStartTime, RaceEndTime

# Constants
DT = RaceEndTime - RaceStartTime
_power_coeff = PanelArea * PanelEfficiency

def _calc_solar_irradiance(time: float) -> float:
    """Calculates solar irradiance at a given time using a Gaussian model."""
    return 1073.099 * np.exp(-0.5 * ((time - 43200) / 11600)**2)

def calculate_incident_solarpower(globaltime: float, latitude: float, longitude: float) -> float:
    """Calculates incident solar power in Wh at a specific global time."""
    gt = globaltime % DT
    intensity = _calc_solar_irradiance(RaceStartTime + gt)
    return intensity * _power_coeff / 3600

def integrand(t: float) -> float:
    """Integrand function for energy calculation (Solar Power in Wh)."""
    intensity = _calc_solar_irradiance(t)
    return intensity * _power_coeff / 3600

def calculate_energy(interval_start: float, interval_end: float) -> float:
    """Calculates total solar energy in Wh generated between two time stamps.

    Args:
        interval_start: Start time in seconds.
        interval_end: End time in seconds.

    Returns:
        Total energy in Wh.
    """
    energy, _ = quad(integrand, interval_start, interval_end)
    return energy

if __name__ == '__main__':
    # Diagnostic check for energy generation
    energy_6_9_am = calculate_energy(6 * 3600, 9 * 3600)
    energy_5_6_pm = calculate_energy(17 * 3600, 18 * 3600)

    print(f"Energy generated from 6-9 AM: {energy_6_9_am:.2f} Wh")
    print(f"Energy generated from 5-6 PM: {energy_5_6_pm:.2f} Wh")
