import numpy as np

from race_config import BatteryCapacity
import state
from car import calculate_dt, calculate_power
from solar import calculate_incident_solarpower

def extract_profiles(velocity_profile: np.ndarray, segment_array: np.ndarray, 
                     slope_array: np.ndarray, latitude_array: np.ndarray, 
                     longitude_array: np.ndarray, winds_array: np.ndarray, 
                     winddir_array: np.ndarray) -> list[np.ndarray]:
    """Extracts detailed simulation profiles for plotting and analysis.

    Returns:
        list of np.ndarray: [distances, velocities, accelerations, battery_levels, 
                            energy_consumptions, solar_gains, time_stamps]
    """
    v_start, v_stop = velocity_profile[:-1], velocity_profile[1:]
    avg_speed = (v_start + v_stop) / 2
    
    # Calculate intervals
    dt = calculate_dt(v_start, v_stop, segment_array)
    acceleration = (v_stop - v_start) / dt

    # Power and solar calculations
    net_power, _ = calculate_power(avg_speed, acceleration, slope_array, winds_array, winddir_array)
    solar_power = calculate_incident_solarpower(
        dt.cumsum() + state.TimeOffset, latitude_array, longitude_array
    )

    energy_consumption = net_power * dt / 3600
    solar_gain = solar_power * dt / 3600

    net_energy_delta = energy_consumption.cumsum() - solar_gain.cumsum()
    
    battery_charge_wh = state.InitialBatteryCapacity - net_energy_delta
    battery_levels = np.concatenate(([state.InitialBatteryCapacity], battery_charge_wh))

    # Convert to percentage
    battery_percent = battery_levels * 100 / BatteryCapacity

    dist_points = np.append([0], segment_array)

    return [
        dist_points,
        velocity_profile,
        np.concatenate(([np.nan], acceleration)),
        battery_percent,
        np.concatenate(([np.nan], energy_consumption)),
        np.concatenate(([np.nan], solar_gain)),
        np.concatenate(([0], dt.cumsum())) + state.TimeOffset,
    ]