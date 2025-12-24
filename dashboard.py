import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import race_config as config

# Custom CSS styles
custom_styles = {
    'font-family': '"Quicksand", sans-serif',
    'background-color': '#f0f0f0',
    'text-align': 'center',
    'margin': '10px',
    'padding': '10px',
    'border': '1px solid #ccc',
    'border-radius': '5px'
}

# Extra CSS style sheets
external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Quicksand:wght@300..700&family=Roboto+Slab:wght@100..900&family=Space+Grotesk:wght@300..700&display=swap",
]

# Initialize Dash app
def create_app(distances, velocity_profile, acceleration_profile, battery_profile, energy_consumption_profile, solar_profile, time):
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    
    avg_vel = distances[-1] / (time[-1] - 4.5 * 3600) if (time[-1] - 4.5 * 3600) != 0 else 0
    
    app.layout = html.Div([
        # Header Section
        html.Div([
            html.Img(
                src='https://cfi.iitm.ac.in/assets/Agnirath-456b8655.png',
                style={
                    'height': '60px',
                    'margin-right': '10px',
                    'border': '1px solid #fe602c',
                    'border-radius': '50%',
                    'background-color': '#000000',
                }
            ),
            html.H1("Strategy Analysis Dashboard", style={'text-align': 'center', 'font-family': '"Roboto Slab", serif'}),
        ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center', 'align-items': 'center'}),

        # Full Configuration Parameters Section
        html.Div([
            html.H2("Configuration Parameters", style={'text-align': 'center', 'font-family': '"Space Grotesk", sans-serif'}),
            html.Div([
                html.Div([
                    html.P(f"Battery Capacity: {config.BatteryCapacity} Wh"),
                    html.P(f"Deep Discharge: {config.DeepDischargeCap}"),
                    html.P(f"Mass: {config.Mass} kg"),
                    html.P(f"Wheels: {config.Wheels}"),
                    html.P(f"Bus Voltage: {config.BusVoltage} V"),
                ], style={'width': '33%'}),
                html.Div([
                    html.P(f"Cd: {config.Cd}"),
                    html.P(f"Frontal Area: {config.FrontalArea} m^2"),
                    html.P(f"Solar Area: {config.PanelArea} m^2"),
                    html.P(f"Solar Efficiency: {config.PanelEfficiency}"),
                    html.P(f"Zero Speed Crr: {config.ZeroSpeedCrr}"),
                ], style={'width': '33%'}),
                html.Div([
                    html.P(f"Air Density: {config.AirDensity} kg/m^3"),
                    html.P(f"Gravity: {config.GravityAcc} m/s^2"),
                    html.P(f"Max Velocity: {config.MaxVelocity} m/s"),
                    html.P(f"Ambient Temp: {config.Ta} K"),
                    html.P(f"Air Viscosity: {config.AirViscosity}"),
                ], style={'width': '33%'}),
            ], style={'display': 'flex', 'justify-content': 'center', 'text-align': 'left'})
        ], style={'width': '80%', 'margin': 'auto', 'padding': '20px', 'border': '1px solid #ccc', 'border-radius': '5px'}),
       
        # Graphs Grid
        html.Div([
            # Velocity Profiles
            dcc.Graph(
                id='velocity-profile',
                figure={
                    'data': [
                        go.Scatter(x=distances, y=velocity_profile, mode='lines+markers', name='Velocity (m/s)'),
                        go.Scatter(x=[min(distances), max(distances)], y=[config.MaxVelocity, config.MaxVelocity], mode='lines', name="Max Velocity", line=dict(color='red', dash='dot')),
                        go.Scatter(x=[min(distances), max(distances)], y=[avg_vel, avg_vel], mode='lines', name="Avg Velocity", line=dict(color='green', dash='dot')),
                    ],
                    'layout': go.Layout(title='Velocity Profile (m/s)', xaxis={'title': 'Distance (m)'}, yaxis={'title': 'm/s'})
                },
                style={'width': '93%', 'display': 'inline-block', **custom_styles}
            ),
            dcc.Graph(
                id='kmphvelocity-profile',
                figure={
                    'data': [
                        go.Scatter(x=distances, y=velocity_profile * 3.6, mode='lines+markers', name='Velocity (km/h)'),
                        go.Scatter(x=[min(distances), max(distances)], y=[config.MaxVelocity * 3.6, config.MaxVelocity * 3.6], mode='lines', name="Max Velocity", line=dict(color='red', dash='dot')),
                        go.Scatter(x=[min(distances), max(distances)], y=[avg_vel * 3.6, avg_vel * 3.6], mode='lines', name="Avg Velocity", line=dict(color='green', dash='dot')),
                    ],
                    'layout': go.Layout(title='Velocity Profile (km/h)', xaxis={'title': 'Distance (m)'}, yaxis={'title': 'km/h'})
                },
                style={'width': '93%', 'display': 'inline-block', **custom_styles}
            ),

            # Summary and Analysis
            html.Div([
                html.Div([
                    html.H2("Summary", style={'text-align': 'center', 'font-family': '"Space Grotesk", sans-serif'}),
                    html.P(f"Total Distance: {round(distances[-1] / 1000, 3)} km"),
                    html.P(f"Time Taken: {time[-1] // 3600}hrs {(time[-1] % 3600) // 60}mins {round(((time[-1] % 3600) % 60), 3)}secs"),
                    html.P(f"No of points: {len(distances)}pts"),
                ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top', **custom_styles}),
                html.Div([
                    html.H2("Data Analysis", style={'text-align': 'center', 'font-family': '"Space Grotesk", sans-serif'}),
                    html.P(f"Max Velocity: {round(max(velocity_profile), 3)} m/s ({round(max(velocity_profile)*3.6, 2)} km/h)"),
                    html.P(f"Avg Velocity: {round(avg_vel, 3)} m/s ({round(avg_vel*3.6, 2)} km/h)"),
                    html.P(f"Average Battery Level: {sum(battery_profile) / len(battery_profile):.2f}%")
                ], style={'width': '60%', 'display': 'inline-block', 'vertical-align': 'top', **custom_styles}),
            ], style={'width': '93%', 'display': 'flex', 'justify-content': 'center'}),

            # Physics Profiles
            dcc.Graph(
                id='acceleration-profile',
                figure={
                    'data': [go.Scatter(x=distances[1:], y=acceleration_profile[1:], mode='lines+markers', name='Acceleration')],
                    'layout': go.Layout(title='Acceleration Profile', xaxis={'title': 'Distance (m)'}, yaxis={'title': 'm/s^2'})
                },
                style={'width': '45%', 'display': 'inline-block', **custom_styles}
            ),
            dcc.Graph(
                id='battery-profile',
                figure={
                    'data': [
                        go.Scatter(x=distances, y=battery_profile, mode='lines+markers', name='Battery %'),
                        go.Scatter(x=[min(distances), max(distances)], y=[100, 100], mode='lines', name="Max", line=dict(color='red', dash='dot')),
                        go.Scatter(x=[min(distances), max(distances)], y=[config.DeepDischargeCap * 100, config.DeepDischargeCap * 100], mode='lines', name="Min", line=dict(color='orange', dash='dot')),
                    ],
                    'layout': go.Layout(title='Battery Level Profile', xaxis={'title': 'Distance (m)'}, yaxis={'title': 'Charge (%)'})
                },
                style={'width': '45%', 'display': 'inline-block', **custom_styles}
            ),

            # Energy Consumption
            dcc.Graph(
                id='energy-consumption-profile',
                figure={
                    'data': [go.Scatter(x=distances[1:], y=energy_consumption_profile[1:], mode='lines+markers', name='Energy (Wh)')],
                    'layout': go.Layout(title='Segment Energy Consumption', xaxis={'title': 'Distance (m)'}, yaxis={'title': 'Wh'})
                },
                style={'width': '45%', 'display': 'inline-block', **custom_styles}
            ),
            dcc.Graph(
                id='net-energy-consumption-profile',
                figure={
                    'data': [go.Scatter(x=distances[1:], y=energy_consumption_profile[1:].cumsum(), mode='lines+markers', name='Net Energy (Wh)')],
                    'layout': go.Layout(title='Cumulative Energy Consumption', xaxis={'title': 'Distance (m)'}, yaxis={'title': 'Wh'})
                },
                style={'width': '45%', 'display': 'inline-block', **custom_styles}
            ),

            # Solar Gain
            dcc.Graph(
                id='solar-profile',
                figure={
                    'data': [go.Scatter(x=distances[1:], y=solar_profile[1:], mode='lines+markers', name='Solar (Wh)')],
                    'layout': go.Layout(title='Segment Solar Gain', xaxis={'title': 'Distance (m)'}, yaxis={'title': 'Wh'})
                },
                style={'width': '45%', 'display': 'inline-block', **custom_styles}
            ),
            dcc.Graph(
                id='net-solar-profile',
                figure={
                    'data': [go.Scatter(x=distances[1:], y=solar_profile[1:].cumsum(), mode='lines+markers', name='Net Solar (Wh)')],
                    'layout': go.Layout(title='Cumulative Solar Gain', xaxis={'title': 'Distance (m)'}, yaxis={'title': 'Wh'})
                },
                style={'width': '45%', 'display': 'inline-block', **custom_styles}
            ),

            # Time Profile
            dcc.Graph(
                id='time-profile',
                figure={
                    'data': [go.Scatter(x=distances, y=time / 3600, mode='lines+markers', name='Time (hrs)')],
                    'layout': go.Layout(title='Time vs Distance', xaxis={'title': 'Distance (m)'}, yaxis={'title': 'Total Time (hrs)'})
                },
                style={'width': '93%', 'display': 'inline-block', **custom_styles}
            ),
        ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center'})
    ], style={'background-color': '#ffffff', 'padding': '20px'})
    
    return app

if __name__ == '__main__':
    # Load and clean simulation data
    try:
        output_df = pd.read_csv("run_dat.csv").fillna(0)
        # Handle cases where column names might differ (e.g., lowercase/uppercase)
        cols = {c.lower(): c for c in output_df.columns}
        
        dist = output_df[cols.get('cumulativedistance', output_df.columns[0])].to_numpy()
        vel = output_df[cols.get('velocity', output_df.columns[1])].to_numpy()
        acc = output_df[cols.get('acceleration', output_df.columns[2])].to_numpy()
        batt = output_df[cols.get('battery', output_df.columns[3])].to_numpy()
        energy = output_df[cols.get('energyconsumption', output_df.columns[4])].to_numpy()
        solar = output_df[cols.get('solar', output_df.columns[5])].to_numpy()
        t = output_df[cols.get('time', output_df.columns[6])].to_numpy()
        
        dist_cumulative = dist.cumsum()
        
        # Initialize and run dashboard
        dashboard_app = create_app(dist_cumulative, vel, acc, batt, energy, solar, t)
        dashboard_app.run(debug=True)
    except Exception as e:
        print(f"Error loading dashboard data: {e}")
        print("Ensure 'run_dat.csv' exists and has correct columns.")
