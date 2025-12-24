import numpy as np
import race_config as config
from race_config import BatteryCapacity, DeepDischargeCap, MaxVelocity, Mass, MaxCurrent, BusVoltage
import state
from car import calculate_dt, calculate_power
from solar import calculate_incident_solarpower

SafeBatteryLevel = BatteryCapacity * DeepDischargeCap
MaxPower = MaxCurrent * BusVoltage

def _trim_arrays(*arrays: np.ndarray) -> list[np.ndarray]:
    """Trims multiple arrays to the length of the shortest among them."""
    min_len = min(len(a) for a in arrays)
    return [a[:min_len] for a in arrays]

def get_bounds(n_segments: int) -> list[tuple[float, float]]:
    """Returns velocity bounds for the optimization.
    
    The car starts and ends at 0 velocity, and stays within MaxVelocity during the race.
    """
    return ([(0, 0)] + [(0.01, MaxVelocity)] * (n_segments - 2) + [(0, 0)])

def objective(velocity_profile: np.ndarray, segment_array: np.ndarray) -> float:
    """Calculates total race time (the objective to minimize)."""
    v_start, v_stop, segments = _trim_arrays(velocity_profile[:-1], velocity_profile[1:], segment_array)
    dt = calculate_dt(v_start, v_stop, segments)
    return float(np.sum(dt))

def battery_acc_constraint_func(v_prof: np.ndarray, segment_array: np.ndarray, 
                                slope_array: np.ndarray, latitude_array: np.ndarray, 
                                longitude_array: np.ndarray, wind_speed: np.ndarray, 
                                wind_dir: np.ndarray) -> tuple[float, float]:
    """Ensures battery doesn't deplete and power doesn't exceed MaxPower."""
    v_start, v_stop, segments, slopes, lats, longs, ws, wd = _trim_arrays(
        v_prof[:-1], v_prof[1:], segment_array, slope_array, 
        latitude_array, longitude_array, wind_speed, wind_dir
    )
    
    avg_speed = (v_start + v_stop) / 2
    dt = calculate_dt(v_start, v_stop, segments)
    acceleration = (v_stop - v_start) / dt

    net_power, _ = calculate_power(avg_speed, acceleration, slopes, ws, wd)
    solar_power = calculate_incident_solarpower(dt.cumsum() + state.TimeOffset, lats, longs)

    energy_consumption = ((net_power - solar_power) * dt).cumsum() / 3600
    battery_profile = state.InitialBatteryCapacity - energy_consumption - SafeBatteryLevel

    return float(np.min(battery_profile)), float(MaxPower - np.max(net_power))

def final_battery_constraint_func(v_prof: np.ndarray, segment_array: np.ndarray, 
                                  slope_array: np.ndarray, latitude_array: np.ndarray, 
                                  longitude_array: np.ndarray, wind_speed: np.ndarray, 
                                  wind_dir: np.ndarray) -> tuple[float, float]:
    """Ensures final battery level meets the strategy target."""
    v_start, v_stop, segments, slopes, lats, longs, ws, wd = _trim_arrays(
        v_prof[:-1], v_prof[1:], segment_array, slope_array, 
        latitude_array, longitude_array, wind_speed, wind_dir
    )
    
    avg_speed = (v_start + v_stop) / 2
    dt = calculate_dt(v_start, v_stop, segments)
    acceleration = (v_stop - v_start) / dt

    net_power, _ = calculate_power(avg_speed, acceleration, slopes, ws, wd)
    solar_power = calculate_incident_solarpower(dt.cumsum() + state.TimeOffset, lats, longs)

    energy_consumption = ((net_power - solar_power) * dt).cumsum() / 3600
    final_battery_lev = state.InitialBatteryCapacity - energy_consumption[-1] - state.FinalBatteryCapacity
    return float(final_battery_lev), float(-final_battery_lev)
