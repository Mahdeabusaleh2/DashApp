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

# Layout for the app
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
        html.P("Radiation – the word sounds scary. But what is it really? "
               "Would it surprise you to know that you experience radiation every day? "
               "Radiation can be broadly defined as energy that travels in waves or particles. "),
        html.P("Non-Ionizing Radiation is low energy in nature, so it is generally safe. "
               "This type of radiation shows up in your everyday life as microwaves, radio waves, and visible light."),
        html.P("The higher energy of Ionizing Radiation allows it to kick out electrons from an atom. "
               "X-rays and gamma rays (and some UV rays) are examples of ionizing radiation. "
               "This type of radiation can be potentially harmful to a human."),
        html.P("We are exposed to low levels of X-rays when we have an X-ray image of our bones. "
               "CAT scans and Mammograms also use X-rays to image our bodies."),
        html.P("We encounter Gamma Rays in small amounts if we have a PET scan or if we travel in an airplane. "
               "Solar flares also emit gamma rays that can reach the earth. "
               "Some other natural sources of gamma rays are from naturally occurring radon gas "
               "and trace amounts of uranium ore in our soil."),
        html.P("For the most part, even the ionizing radiation we experience on a daily basis is harmless. "
               "However, long-term exposure to these low dose sources can accumulate and potentially affect us "
               "in different ways. We address some of those sources as well as the potential effects of such exposure.")
    ]),

    # Radiation Exposure Section
    html.Div(id='exposure', children=[
        html.H3("Radiation Exposure from Common Sources"),
        dcc.Graph(
            figure={
                "data": [go.Bar(x=df["Source"], y=df["Dose (mSv)"], marker_color='blue')],
                "layout": go.Layout(title="Radiation Dose Comparison (mSv)", xaxis_title="Source",
                                    yaxis_title="Dose (mSv)")
            }
        ),
    ]),

    # Dose-Response Models Section (Only LNT)
    html.Div(id='models', children=[
        html.H3("Dose-Response Models: LNT"),
        dcc.Graph(
            figure={
                "data": [
                    go.Scatter(x=dose_values, y=lnt_risk, mode='lines', name='Linear No-Threshold (LNT)',
                               line=dict(color='red')),
                ],
                "layout": go.Layout(title="Radiation Dose-Response Model (LNT Only)", 
                                    xaxis_title="Radiation Dose (mSv)", 
                                    yaxis_title="Relative Risk")
            }
        ),
    ]),

    # FAQ Section
    html.Div(id='faq', children=[
        html.H3("Frequently Asked Questions (FAQ)"),
        html.Details([
            html.Summary("What are Sv and mSv?"),
            html.P("Sv = Sievert, which is 1 Joule per kilogram. mSv = millisievert, which is 1/1000 of a Sv."),
        ]),
        html.Details([
            html.Summary("What is background radiation? Is it harmful?"),
            html.P("Background radiation is natural and includes cosmic, terrestrial, and internal sources. "
                   "At normal exposure levels, it is not harmful."),
        ]),
        html.Details([
            html.Summary("How does radiation affect air travel?"),
            html.P("Radiation exposure increases at higher altitudes. A flight from NYC to LA results in about 0.04 mSv."),
        ]),
        html.Details([
            html.Summary("Is radiation from medical imaging safe?"),
            html.P("Medical imaging, such as CT scans and X-rays, delivers ionizing radiation in controlled environments."),
        ]),
    ]),

    # References Section
    html.Div(id='references', children=[
        html.H3("References"),
        html.Ul([
            html.Li(html.A("Health Physics Society", href="https://hps.org/hpspublications/radiationfactsheets.html", target="_blank")),
            html.Li(html.A("International Commission on Radiological Protection (ICRP)", href="https://www.icrp.org/page.asp?id=5", target="_blank")),
            html.Li(html.A("National Council on Radiation Protection and Measurements (NCRP)", href="https://ncrponline.org/", target="_blank")),
        ]),
    ]),

    # Conclusion Section
    html.Div(id='conclusion', children=[
        html.H3("Conclusion"),
        html.P("Radiation is a part of everyday life, and complete avoidance is neither necessary nor possible."),
        html.P("By understanding exposure sources and risk models, we can make informed choices without unnecessary fear."),
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

])  # ✅ Ensuring proper closure of `app.layout`

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=True, host="0.0.0.0", port=port)
