import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import os  # Required for Render deployment

# Initialize the Dash app
app = dash.Dash(__name__)

# Radiation exposure data (in millisieverts, mSv)
radiation_sources = {
    "Background Radiation (Annual Avg)": 3.0,
    "Chest X-ray": 0.1,
    "Dental X-ray": 0.005,
    "Mammogram": 0.4,
    "CT Scan (Abdomen)": 8.0,
    "Flight (NYC to LA)": 0.04,
    "Smoking (1 pack/day, Annual)": 70.0,
    "Fukushima Evacuation Zone (Annual)": 12.0,
}

df = pd.DataFrame(list(radiation_sources.items()), columns=["Source", "Dose (mSv)"])

# Define dose values
dose_values = np.linspace(0, 100, 100)

# LNT Model: Risk increases linearly with dose
lnt_risk = dose_values * 0.01

# Layout for the app (EVERYTHING INSIDE app.layout)
app.layout = html.Div([
    html.H1("Understanding Radiation Exposure and Risk", style={'textAlign': 'center'}),

    # Navigation Bar
    html.Div([
        html.A('Exposure Sources | ', href='#exposure', style={'cursor': 'pointer', 'textDecoration': 'none'}),
        html.A('Dose-Response Models | ', href='#models', style={'cursor': 'pointer', 'textDecoration': 'none'}),
        html.A('Calculator | ', href='#calculator', style={'cursor': 'pointer', 'textDecoration': 'none'}),
        html.A('FAQ | ', href='#faq', style={'cursor': 'pointer', 'textDecoration': 'none'}),
        html.A('Conclusion', href='#conclusion', style={'cursor': 'pointer', 'textDecoration': 'none'})
    ], style={'textAlign': 'center', 'marginBottom': 20}),

    # Introduction Section
    html.Div(id="introduction", children=[
        html.H3("Introduction"),
        html.P("Radiation – the word sounds scary. But what is it really? ..."),
    ]),

    # Exposure Sources Section
    html.Div(id='exposure', children=[
        html.H3("Radiation Exposure from Common Sources"),
        dcc.Graph(
            figure={
                "data": [go.Bar(x=df["Source"], y=df["Dose (mSv)"], marker_color='blue')],
                "layout": go.Layout(title="Radiation Dose Comparison (mSv)", xaxis_title="Source",
                                    yaxis_title="Dose (mSv)")
            }
        ),
        html.P("The chart above compares radiation doses from common sources, providing insight into relative exposure levels."),
    ]),

    # Dose-Response Models (Only LNT)
    html.Div(id='models', children=[
        html.H3("Dose-Response Model: LNT"),
        dcc.Graph(
            figure={
                "data": [go.Scatter(x=dose_values, y=lnt_risk, mode='lines', name='Linear No-Threshold (LNT)',
                                    line=dict(color='red'))],
                "layout": go.Layout(title="Radiation Dose-Response Model (LNT Only)", 
                                    xaxis_title="Radiation Dose (mSv)", 
                                    yaxis_title="Relative Risk")
            }
        ),
        html.P("The Linear No-Threshold (LNT) model assumes all radiation exposure carries some risk, "
               "no matter how small."),
    ]),

    # Calculator Section (THIS FIXES THE MISSING ID ERROR)
    html.Div(id='calculator', children=[
        html.H3("Personal Radiation Exposure Calculator"),
        
        html.Label("Number of flights per year (NYC to LA equivalent):"),
        dcc.Slider(0, 50, 1, value=5, marks={i: str(i) for i in range(0, 51, 10)}, id='flight-slider'),

        html.Label("Number of chest X-rays per year:"),
        dcc.Slider(0, 10, 1, value=1, marks={i: str(i) for i in range(0, 11)}, id='xray-slider'),

        html.Div(id='total-dose-output', style={'fontSize': 20, 'marginTop': 20}),
    ]),

    # FAQ Section
    html.Div(id='faq', children=[
        html.H3("Frequently Asked Questions (FAQ)"),
        html.Details([
            html.Summary("What are Sv and mSv?"),
            html.P("Sv = Sievert, which is 1 Joule per kilogram. This is the international system unit for dose equivalent."),
        ]),
    ]),

    # References Section
    html.Div(id='references', children=[
        html.H3("References"),
        html.Ul([
            html.Li(html.A("Health Physics Society",
                        href="https://hps.org/hpspublications/radiationfactsheets.html", target="_blank")),
        ]),
    ]),

    # Conclusion Section
    html.Div(id='conclusion', children=[
        html.H3("Conclusion"),
        html.P("Understanding radiation exposure and risk is important in making informed decisions about health and safety."),
    ]),

    # Video Section
    html.Div(id="video", children=[
        html.H3("Radiation Exposure Explained - Video Resource"),
        html.Iframe(
            src="https://www.youtube.com/embed/uzqsnxZBLNE",
            width="700",
            height="400",
            style={"border": "none", "display": "block", "margin": "auto"}
        )
    ])
])  # ✅ Everything is inside `app.layout`

# Callback for radiation dose calculator (NO MORE MISSING IDS!)
@app.callback(
    Output("total-dose-output", "children"),
    [Input("flight-slider", "value"), Input("xray-slider", "value")]
)
def update_dose(flights, xrays):
    total_dose = (flights * 0.04) + (xrays * 0.1)
    return f"Your estimated annual radiation dose from selected activities: {total_dose:.2f} mSv"

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=True, host="0.0.0.0", port=port)
