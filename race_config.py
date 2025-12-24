# ---------------------------------------------------------------------------------------------------------
# Car Data

# Battery
BatteryCapacity = 3055 # Wh
DeepDischargeCap = 0.2

# Physical Attributes
R_In = 0.214 # inner radius of wheel
R_Out = 0.2785  # outer radius of wheel
Mass = 267 # kg
Wheels = 3
StatorRotorAirGap = 1.5 * 10**-3

# Resistive Coeff
ZeroSpeedCrr = 0.0045
FrontalArea = 1 # m^2
Cd = 0.092# coefficient of drag
CDA = Cd * FrontalArea

# Solar Panel Data
PanelArea = 6 # m^2
PanelEfficiency = 0.19

# Bus Voltage
BusVoltage = 4.2 * 38  # V

# ---------------------------------------------------------------------------------------------------------
# Physical Constants
AirDensity = 1.192 # kg/m^3
g = GravityAcc = 9.81 # m/s^2
AirViscosity = 1.524 * 10**-5  # kinematic viscosity of air
Ta = 295
EPSILON = 10**-8

# ---------------------------------------------------------------------------------------------------------
# Race Strategy & Waypoints
# BatteryLevelWayPoints = [1, 0.4994, 0.5, 0.2543, 0.488, 0.2276, 0.408, 0.2410, 0.27, 0.2393, 0.22]
# BatteryLevelWayPoints = [1,0.44,0.51,0.5,0.2543,0.488,0.48,0.3276,0.408,0.39,0.2410,0.28,0.33,0.22]
BatteryLevelWayPoints = [1, 0.44, 0.51, 0.5, 0.2543, 0.488, 0.48, 0.3276, 0.408, 0.39, 0.2410, 0.299, 0.43, 0.22]

# DF_WayPoints = [0, 57, 102, 169, 207, 254, 301, 371, 415, 464, 520]
# DF_WayPoints = [0, 57, 102, 109, 169, 207, 213, 254, 301, 308, 371, 415, 464, 520]
DF_WayPoints = [0, 57, 102, 109, 169, 207, 213, 254, 301, 308, 371, 415, 464, 520]
# DF_WayPoints = [0, 57*2, 102*2, 109*2, 169*2, 207*2, 213*2, 254*2, 301*2, 308*2, 371*2, 415*2, 464*2, 520*2]
DayEnd_WayPoints = [109, 213, 308, 415, 520]
# DayEnd_WayPoints = [109*2, 213*2, 308*2, 415*2, 520*2]


# ---------------------------------------------------------------------------------------------------------
# Simulation Settings
ModelMethod = "COBYLA"
InitialGuessVelocity = 25

RaceStartTime = 8 * 3600  # 8:00 am
RaceEndTime = (17) * 3600  # 5:00 pm
DT = RaceEndTime - RaceStartTime

CONTROL_STOP_DURATION = 30 * 60

# Car Constraints
MaxVelocity = 35 # m/s
MaxCurrent = 12.3  # Am
MaxAcc=0.1