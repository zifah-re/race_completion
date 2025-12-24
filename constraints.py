import numpy as np

from config import BatteryCapacity, DeepDischargeCap, MaxVelocity, Mass, MaxCurrent, BusVoltage
import state
from car import calculate_dt, calculate_power
from solar import calculate_incident_solarpower

SafeBatteryLevel = BatteryCapacity * (DeepDischargeCap)
MaxPower = MaxCurrent * BusVoltage

# Bounds for the velocity
def get_bounds(N):
    return ([(0, 0)] + [(0.01, MaxVelocity)]*(N-2) + [(0, 0)])

def objective(velocity_profile, segment_array):
    start_speeds = velocity_profile[:-1]
    stop_speeds = velocity_profile[1:]
    
    # Fix for array shape mismatch
    min_len = min(len(start_speeds), len(segment_array))
    start_speeds = start_speeds[:min_len]
    stop_speeds = stop_speeds[:min_len]
    segment_array = segment_array[:min_len]

    dt = calculate_dt(start_speeds, stop_speeds, segment_array)
    return np.sum(dt)

def battery_acc_constraint_func(v_prof, segment_array, slope_array, lattitude_array, longitude_array,ws,wd):
    start_speeds, stop_speeds = v_prof[:-1], v_prof[1:]
    
    # Fix for array shape mismatch
    # print("DEBUG: Trimming arrays in battery_acc_constraint_func")
    min_len = min(len(start_speeds), len(segment_array))
    start_speeds = start_speeds[:min_len]
    stop_speeds = stop_speeds[:min_len]
    segment_array = segment_array[:min_len]
    slope_array = slope_array[:min_len]
    lattitude_array = lattitude_array[:min_len]
    longitude_array = longitude_array[:min_len]
    ws = ws[:min_len]
    wd = wd[:min_len]
    
    avg_speed = (start_speeds + stop_speeds) / 2
    
    dt = calculate_dt(start_speeds, stop_speeds, segment_array)
    acceleration = (stop_speeds - start_speeds) / dt

    P, PO = calculate_power(avg_speed, acceleration, slope_array,ws,wd)
    SolP = calculate_incident_solarpower(dt.cumsum() + state.TimeOffset, lattitude_array, longitude_array)

    energy_consumption = ((P - SolP) * dt).cumsum() / 3600
    battery_profile = state.InitialBatteryCapacity - energy_consumption - SafeBatteryLevel

    return np.min(battery_profile), MaxPower - np.max(P)

def final_battery_constraint_func(v_prof, segment_array, slope_array, lattitude_array, longitude_array,ws,wd):
    start_speeds, stop_speeds = v_prof[:-1], v_prof[1:]
    
    # Fix for array shape mismatch
    min_len = min(len(start_speeds), len(segment_array))
    start_speeds = start_speeds[:min_len]
    stop_speeds = stop_speeds[:min_len]
    segment_array = segment_array[:min_len]
    slope_array = slope_array[:min_len]
    lattitude_array = lattitude_array[:min_len]
    longitude_array = longitude_array[:min_len]
    ws = ws[:min_len]
    wd = wd[:min_len]
    
    avg_speed = (start_speeds + stop_speeds) / 2
    dt = calculate_dt(start_speeds, stop_speeds, segment_array)
    acceleration = (stop_speeds - start_speeds) / dt

    P, _= calculate_power(avg_speed, acceleration, slope_array,ws,wd)
    SolP = calculate_incident_solarpower(dt.cumsum() + state.TimeOffset, lattitude_array, longitude_array)

    energy_consumption = ((P - SolP) * dt).cumsum() / 3600
    final_battery_lev = state.InitialBatteryCapacity - energy_consumption[-1] - state.FinalBatteryCapacity
    return final_battery_lev, -final_battery_lev