import race_config as config
import pandas as pd

Day=1
TimeOffset = 0

InitialBatteryCapacity = None
FinalBatteryCapacity = None
route_df = None

def set_day_state(day_no, index_no, time_offset=0):
    global InitialBatteryCapacity, FinalBatteryCapacity, route_df, Day, TimeOffset
    Day = day_no
    TimeOffset = time_offset
    InitialBatteryCapacity = config.BatteryCapacity * config.BatteryLevelWayPoints[index_no] # Wh
    FinalBatteryCapacity = config.BatteryCapacity * config.BatteryLevelWayPoints[index_no+1]  # Wh
    route_df = pd.read_csv("processed_route_data.csv").iloc[config.DF_WayPoints[index_no]: config.DF_WayPoints[index_no+1]]
