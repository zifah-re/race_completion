import pandas as pd
import numpy as np

import state
import race_config as config
from model import main as run_model_main
from offrace_solar_calc import calculate_energy


def main() -> None:
    """Orchestrates the multi-day race simulation and saves aggregated results."""
    results_list = []
    current_day = 1
    total_time = 0.0
    energy_stop_gain = 0.0

    print("--- Starting Full Race Simulation ---")

    for waypoint_idx in range(13):
        # Check if we are at a standard waypoint or a day-end waypoint
        is_day_end = config.DF_WayPoints[waypoint_idx + 1] in config.DayEnd_WayPoints
        
        state.set_day_state(current_day, waypoint_idx, total_time)
        
        # Add energy gained during charging at the stop to initial battery for the segment
        state.InitialBatteryCapacity = min(
            config.BatteryCapacity, 
            energy_stop_gain + state.InitialBatteryCapacity
        )
        
        print(f"Running Segment {waypoint_idx + 1}/13 (Day {current_day})...")
        segment_df, segment_time = run_model_main(state.route_df)
        results_list.append(segment_df)
        total_time += segment_time

        if not is_day_end:
            # Short control stop energy gain calculation
            energy_stop_gain = calculate_energy(
                total_time, 
                total_time + config.CONTROL_STOP_DURATION
            )
            total_time += config.CONTROL_STOP_DURATION
        else:
            # End of day energy gain calculation (e.g., overnight/morning charging)
            # Strategy: Charge between 5 PM - 6 PM and 5 AM - 8 AM
            energy_stop_gain = calculate_energy(17 * 3600, 18 * 3600)
            energy_stop_gain += calculate_energy(5 * 3600, 8 * 3600)
            current_day += 1

    # Aggregate and save results
    full_race_df = pd.concat(results_list)
    full_race_df.to_csv('run_dat.csv', index=False)
    
    print("--- Simulation Complete ---")
    print(f"Results saved to `run_dat.csv` ({len(full_race_df)} records)")

if __name__ == "__main__":
    main()
