import numpy as np
from scipy.optimize import minimize
import pandas as pd

import race_config as config
import state
from constraints import get_bounds, objective, battery_acc_constraint_func, final_battery_constraint_func
from profiles import extract_profiles

def main(route_df: pd.DataFrame) -> tuple[pd.DataFrame, float]:
    """Runs the simulation for a single race segment.

    Args:
        route_df: DataFrame containing segment data (distance, slope, coords, winds).

    Returns:
        tuple: (out_df, time_taken)
    """
    # Extract route data to arrays
    segment_array = route_df.iloc[:, 0].to_numpy()
    slope_array = route_df.iloc[:, 2].to_numpy()
    latitude_array = route_df.iloc[:, 3].to_numpy()
    longitude_array = route_df.iloc[:, 4].to_numpy()
    wind_speed = route_df.iloc[:, 5].to_numpy()
    wind_dir = route_df.iloc[:, 6].to_numpy()

    # Initial guess for optimization
    n_points = len(route_df) + 1
    v_initial = np.concatenate([[0], np.ones(n_points - 2) * config.InitialGuessVelocity, [0]])

    bounds = get_bounds(n_points)
    constraints = [
        {
            "type": "ineq",
            "fun": battery_acc_constraint_func,
            "args": (
                segment_array, slope_array, latitude_array, longitude_array, wind_speed, wind_dir
            )
        },
    ]

    print(f"Starting Optimization (Method: {config.ModelMethod})")
    print("=" * 60)

    # Solver options based on method
    options = {}
    if config.ModelMethod == 'SLSQP':
        options['verbose'] = 3
    elif config.ModelMethod == 'COBYLA':
        options['disp'] = True

    result = minimize(
        objective, v_initial,
        args=(segment_array,),
        bounds=bounds,
        method=config.ModelMethod,
        constraints=constraints,
        options=options
    )
    
    v_optimized = np.array(result.x)
    time_taken = objective(v_optimized, segment_array)

    print("done.")
    print(f"Segment Race Time: {time_taken/3600:.4f} hrs")

    # Generate detailed output data
    profiles = extract_profiles(
        v_optimized, segment_array, slope_array, latitude_array, longitude_array, wind_speed, wind_dir
    )
    
    out_df = pd.DataFrame(
        dict(zip(
            ['CumulativeDistance', 'Velocity', 'Acceleration', 'Battery', 'EnergyConsumption', 'Solar', 'Time'],
            profiles
        ))
    )
    
    return out_df, time_taken

if __name__ == "__main__":
    outdf, _ = main(state.route_df)
    outdf.to_csv('run_dat.csv', index=False)
    print("Written results to `run_dat.csv`")