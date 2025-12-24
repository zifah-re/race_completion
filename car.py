import numpy as np

from race_config import (
    Mass, ZeroSpeedCrr, AirDensity, CDA, R_Out, Ta,
    GravityAcc, EPSILON
)

# Constants
_FRICTIONAL_TORQUE_COEFF = R_Out * Mass * GravityAcc * ZeroSpeedCrr
_DRAG_COEFF_BASE = 0.5 * CDA * AirDensity * (R_Out ** 3)
_DRAG_COEFF = _DRAG_COEFF_BASE / (R_Out ** 2)
_SLOPE_COEFF = Mass * GravityAcc
_WINDAGE_LOSS_COEFF = (170.4 * 10**-6) / (R_Out ** 2)

def calculate_power(speed: np.ndarray, acceleration: np.ndarray, slope: np.ndarray, 
                    wind_speed: np.ndarray, wind_dir: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Calculates net power consumption and output power for the car.

    Renames:
    - tou (torque)
    - Pc (copper ohmic losses)
    - Pe (eddy current losses)
    - Tw (winding temperature)

    Returns:
        tuple: (net_power_clipped, output_power)
    """
    speed2 = speed ** 2

    # Calculate drag torque considering wind speed and relative direction
    drag_torque = _DRAG_COEFF * (speed2 + wind_speed**2 - 2 * speed * wind_speed * np.cos(np.radians(wind_dir)))
    torque = _FRICTIONAL_TORQUE_COEFF * np.cos(np.radians(slope)) + drag_torque
    
    # Thermal iteration for winding temperature and electrical losses
    temp_prev = Ta  # Initial guess for winding temperature

    while True:
        # B = 1.6716 - 0.0006 * (Ta + temp_prev)  # simplified magnetic remanence
        magnetic_remanence = 1.6716 - 0.0006 * (Ta + temp_prev)
        rms_current = 0.561 * magnetic_remanence * torque
        
        # resistance = 0.00022425 * temp_prev - 0.00820525  # winding resistance
        winding_resistance = 0.00022425 * temp_prev - 0.00820525
        
        copper_loss = 3 * rms_current ** 2 * winding_resistance
        eddy_loss = (9.602 * (10**-6) * ((magnetic_remanence / R_Out) ** 2) / winding_resistance) * speed2
        
        winding_temp = 0.455 * (copper_loss + eddy_loss) + Ta
    
        converged = np.abs(winding_temp - temp_prev) < 0.001
        if np.all(converged):
            break

        temp_prev = np.where(converged, temp_prev, winding_temp)

    # Power calculations
    output_power = torque * speed / R_Out
    windage_loss = speed2 * _WINDAGE_LOSS_COEFF
    acceleration_power = (Mass * acceleration + _SLOPE_COEFF * np.sin(np.radians(slope))) * speed

    net_power = output_power + windage_loss + copper_loss + eddy_loss + acceleration_power
    return net_power.clip(0), output_power

def calculate_dt(start_speed: np.ndarray, stop_speed: np.ndarray, dx: np.ndarray) -> np.ndarray:
    """Calculates time interval (dt) between two points given constant acceleration."""
    dt = 2 * dx / (start_speed + stop_speed + EPSILON)
    return dt
