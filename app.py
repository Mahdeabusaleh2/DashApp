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

# Threshold Model: No risk below a certain dose, then linear increase
threshold_dose = 10  # Assume risk starts at 10 mSv
threshold_risk = np.where(dose_values < threshold_dose, 0, (dose_values - threshold_dose) * 0.01)

# Hormesis Model: Beneficial at low doses, harmful at higher doses
hormesis_risk = -0.005 * np.exp(-dose_values / 20) + dose_values * 0.005

# Layout for the app
app.layout = html.Div(
    style={'backgroundColor': 'white', 'padding': '20px'},  # Ensuring a plain white background
    children=[
        html.H1("Understanding Radiation Exposure and Risk", style={'textAlign': 'center'}),
        html.H5("Created by Mahde Abusaleh", style={'textAlign': 'center', 'marginBottom': 20, 'color': 'gray'}),

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
    html.P("""
        Radiation – the word sounds scary. But what is it really? Would it surprise you to know that you experience radiation every day? 
        Radiation can be broadly defined as energy that travels in waves or particles. Radiation is typically broken down into two categories.
    """),
    html.P("""
        Non-Ionizing Radiation is low energy in nature, so it is generally safe. This type of radiation shows up in your everyday life 
        as microwaves, radio waves, and visible light.
    """),
    html.P("""
        The higher energy of Ionizing Radiation allows it to kick out electrons from an atom. X-rays and gamma rays (and some UV rays) 
        are examples of ionizing radiation. This type of radiation can be potentially harmful to a human. We experience these types of 
        radiation usually only in special situations.
    """),
    html.P("""
        We are exposed to low levels of X-rays when we have an x-ray image of our bones. CAT scans and Mammograms also use X-rays to image our bodies.
    """),
    html.P("""
        We encounter Gamma Rays in small amounts if we have a PET scan or if we travel in an airplane. Solar flares also emit gamma rays that can reach the earth. 
        Some other natural sources of gamma rays are from naturally occurring radon gas and trace amounts of uranium ore in our soil.
    """),
    html.P("""
        For the most part, even the ionizing radiation we experience on a daily basis is harmless. However, long-term exposure to these low dose 
        sources can accumulate and potentially affect us in different ways. We address some of those sources as well as the potential effects of such exposure.
    """)
])  # ✅ Ensuring correct indentation and closing brackets


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
            html.P("The chart above compares radiation doses from common sources, providing insight into relative exposure levels."),
        ]),

        # Dose-Response Models Section
        html.Div(id='models', children=[
            html.H3("Dose-Response Models: LNT vs. Threshold vs. Hormesis"),
            dcc.Graph(
                figure={
                    "data": [
                        go.Scatter(x=dose_values, y=lnt_risk, mode='lines', name='Linear No-Threshold (LNT)',
                                   line=dict(color='red')),
                        go.Scatter(x=dose_values, y=threshold_risk, mode='lines', name='Threshold Model',
                                   line=dict(color='blue', dash='dash')),
                        go.Scatter(x=dose_values, y=hormesis_risk, mode='lines', name='Hormesis Model',
                                   line=dict(color='green', dash='dot')),
                    ],
                    "layout": go.Layout(title="Radiation Dose-Response Models", xaxis_title="Radiation Dose (mSv)",
                                        yaxis_title="Relative Risk")
                }
            ),
            html.P("The LNT model assumes all radiation exposure carries some risk, while the Threshold model assumes there is a safe limit."),
            html.P("The Hormesis model suggests that low levels of radiation may be beneficial."),
        ]),

# FAQ Section
html.Div(id='faq', children=[
    html.H3("Frequently Asked Questions (FAQ)"),

    html.Details([
        html.Summary("What are Sv and mSv?"),
        html.P("Sv = Sievert, which is 1 Joule per kilogram. This is the international system unit for dose equivalent. "
               "mSv = millisievert, which is 1/1000 of a Sv."),
        html.P(["Source: U.S. NRC Glossary. ", 
                html.A("Learn more", href="https://www.nrc.gov/reading-rm/basic-ref/glossary/sievert-sv.html", target="_blank")])
    ]),

    html.Details([
        html.Summary("What is background radiation? Is it harmful to me?"),
        html.P("Background radiation is natural radiation that is always present and all around us in the environment. "
               "It includes cosmic radiation (from the sun and stars), terrestrial radiation (from the Earth), "
               "and internal radiation (from all living things)."),
        html.P("Background radiation is NOT harmful at normal exposure levels."),
        html.P(["Source: U.S. NRC Glossary. ", 
                html.A("Learn more", href="https://www.nrc.gov/reading-rm/basic-ref/glossary/background-radiation.html", target="_blank")])
    ]),

    html.Details([
        html.Summary("How does radiation affect air travel?"),
        html.P("Radiation from flying is due to cosmic radiation. If you were to travel from the East Coast to the West Coast, "
               "you would receive 0.035 mSv from the flight."),
        html.P("The longer the flight duration, the more radiation you receive."),
        html.P("The higher the altitude, the higher the dose of radiation."),
        html.P("The further north or south from the equator you fly, the more radiation you will receive."),
        html.P("Overall, air travel results in very low radiation levels."),
        html.P(["Source: CDC Facts About Radiation from Air Travel. ", 
                html.A("Learn more", href="https://www.cdc.gov/radiation-health/data-research/facts-stats/air-travel.html", target="_blank")])
    ]),

    html.Details([
        html.Summary("Is radiation from medical imaging safe?"),
        html.P("Medical imaging, such as CT scans and X-rays, delivers beams in the form of ionizing radiation to a specific part of the body "
               "to visualize internal structures."),
        html.P("Although these involve low radiation doses, the benefits outweigh the potential risks. "
               "These procedures are accomplished in a controlled environment by a professional."),
        html.P("Below 10 mSv, which is a dose rate relevant to radiography, nuclear medicine, and CT scans, "
               "there is no data to support an increase in cancer risk."),
        html.P(["(1) Source: CDC - Radiation in Healthcare: Imaging Procedures. ",
                html.A("Learn more", href="https://www.cdc.gov/radiation-health/features/imaging-procedures.html", target="_blank")]),
        html.P(["(2) Source: National Library of Medicine - Radiation Risk from Medical Imaging. ",
                html.A("Learn more", href="https://www.ncbi.nlm.nih.gov/articles/PMC2996147/#T1", target="_blank")])
    ]),

    html.Details([
        html.Summary("What is the difference between ionizing and non-ionizing radiation?"),
        html.P("Ionizing radiation includes alpha & beta particles, gamma rays, X-rays, neutrons, and high-speed protons. "
               "These particles are capable of producing ions that can potentially damage cells and are considered more energetic than non-ionizing radiation."),
        html.P("Non-ionizing radiation includes radio waves, microwaves, and visible/infrared/UV light. These do not have the ability to produce ions."),
        html.P(["Source: U.S. NRC Glossary. ", 
                html.A("Learn more", href="https://www.nrc.gov/reading-rm/basic-ref/glossary/ionizing-radiation.html", target="_blank")])
    ]),

    html.Details([
        html.Summary("What is radiation hormesis?"),
        html.P("Radiation hormesis is the hypothesis that low doses of ionizing radiation may be beneficial by stimulating physiological performance, "
               "immune competence, and overall health. Although this is a controversial topic in health physics, some studies suggest "
               "that small doses of radiation may increase lifespan."),
        html.P(["Source: Luckey TD. Radiation Hormesis Study. ", 
                html.A("Learn more", href="https://doi.org/10.2203/dose-response.06-102.Luckey", target="_blank")])
    ]),

    html.Details([
        html.Summary("Does radiation exposure always cause cancer?"),
        html.P("No. While high doses and dose rates may cause cancer, there is no public health data that shows an increased occurrence of cancer "
               "due to low radiation doses and low dose rates."),
        html.P(["Source: U.S. NRC - Radiation Exposure and Cancer. ", 
                html.A("Learn more", href="https://www.nrc.gov/about-nrc/radiation/health-effects/rad-exposure-cancer.html", target="_blank")])
    ])
])  # ✅ This ensures the FAQ section is properly closed

# References Section
html.Div(id='references', children=[
    html.H3("References"),
    html.Ul([
        html.Li(html.A("Health Physics Society", 
                       href="https://hps.org/hpspublications/radiationfactsheets.html", target="_blank")),
        html.Li(html.A("International Commission on Radiological Protection (ICRP)", 
                       href="https://www.icrp.org/page.asp?id=5", target="_blank")),
        html.Li(html.A("National Council on Radiation Protection and Measurements (NCRP)", 
                       href="https://ncrponline.org/", target="_blank")),
        html.Li(html.A("BEIR VII Reports", 
                       href="https://nap.nationalacademies.org/resource/11340/beir_vii_final.pdf", target="_blank")),
        html.Li(html.A("National Institutes of Health (NIH)", 
                       href="https://www.nih.gov/", target="_blank")),
        html.Li(html.A("United States Nuclear Regulatory Commission (U.S. NRC)", 
                       href="https://www.nrc.gov/", target="_blank")),
        html.Li(html.A("Centers for Disease Control and Prevention (CDC)", 
                       href="https://www.cdc.gov/", target="_blank")),
    ]),
])  # ✅ This ensures the References section is properly closed

# Conclusion Section
html.Div(id='conclusion', children=[
    html.H3("Conclusion"),
    html.P("""
        Understanding radiation exposure and risk is important in making informed decisions about health and safety. 
        While radiation often has a bad stigma attached to it, as being associated with danger, it is also an essential part of modern life, 
        from medical diagnostics to energy production. By breaking down exposure sources, dose-response models, and personal risk factors, 
        this website aims to provide clarity on this complex subject, helping users navigate the balance between precaution and practicality.
    """),
    html.P("""
        Different models of radiation risk such as the Linear No-Threshold (LNT), Threshold, and Hormesis reflect the ongoing debate among 
        scientists and regulators. The LNT model assumes all exposure carries some risk, while the Threshold model suggests a safe limit, 
        and the Hormesis model argues that low doses may even be beneficial. These perspectives influence safety standards and policies, 
        affecting everything from occupational exposure limits to space exploration guidelines. By understanding these models, 
        individuals can make informed decisions regarding radiation-related risks and make choices based on scientific evidence rather than fear.
    """),
    html.P("""
        In conclusion, radiation is a part of everyday life, and complete avoidance is neither necessary nor possible. 
        Instead, the key is risk awareness and responsible decision-making. Whether considering medical procedures, 
        occupational hazards, or lifestyle choices, having a solid understanding of radiation principles allows individuals to 
        take the correct precautions without unnecessary anxiety. This site serves as a foundation for further exploration and encourages 
        users to continue learning about radiation safety from reliable sources.
    """)
])  # ✅ This ensures the Conclusion section is properly closed

        # Video Section
        html.Div(
            id="video",
            children=[
                html.H3("Radiation Exposure Explained - Video Resource"),
                html.Iframe(
                    src="https://www.youtube.com/embed/uzqsnxZBLNE",
                    width="700",
                    height="400",
                    style={"border": "none", "display": "block", "margin": "auto"}
                )
            ]
        )
    ]
)

# Callback for radiation dose calculator
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
