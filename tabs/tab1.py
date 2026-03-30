# First tab -- main app

# Import
import streamlit as st
import pandas as pd 
import plotly.express as px
from plotly.subplots import make_subplots as sp

def show():
    # Main content
    st.header("Impact Analysis Tool", divider=True)

    # Add columns
    col1, col2 = st.columns([1,4])

    # Column 1: Selection options
    with col1:
        st.subheader("Select Analysis Options")

        impact_category = st.selectbox("Choose an impact method:", 
            ["Carbon Footprint", "ReCiPe Endpoint H", "ReCiPe Midpoint H"])

        outage_frequency = st.selectbox("Choose an outage frequency:", 
            ["Rare (5x/year)", "Moderate outages (10x/yr)", "Frequent outages (20x/yr)"],
            index=1)

        relative_results = st.checkbox("Scale plots to relative values?",value=False)

        st.warning(":building_construction: Add Weighting Factors.")


    # Save the path based on impact category selected.
    if impact_category == "Carbon Footprint":
        PATH = f"./data/GWP100.csv"
    elif impact_category == "ReCiPe Midpoint H":
        PATH = f"./data/ReCiPe-Endpoint.csv"
    else:
        PATH = f"./data/ReCiPe-Endpoint.csv"
    df = pd.read_csv(PATH)  # Save data frame from assigned path

    # Plot the charts
    phases = ["Materials & Mfg", "Transport", "Use", "End-of-Life"]
    midpoints = ["Climate Change", "Ozone Depletion", "Human Toxicity", 
                 "Particulate Matter", "Ionizing Radiation", "Photochemical Oxidant Formation", 
                 "Terrestrial Acidification", "Freshwater Eutrophication", "Marine Eutrophication", 
                 "Terrestrial Ecotoxicity", "Freshwater Ecotoxicity", "Marine Ecotoxicity"]
    units = "kg CO2e" if impact_category == "Carbon Footprint" else "Points"
    col2.subheader(f"{impact_category}")

    # Reduce df based on outage scenario selected
    if outage_frequency == "Rare (5x/year)":
        df = df[df['Outage'] == 'Rare']
    elif outage_frequency == "Moderate outages (10x/yr)":
        df = df[df['Outage'] == 'Moderate']
    else:        
        df = df[df['Outage'] == 'Frequent']
    

    #  Modifications if relative results is selected
    if relative_results:
        bar_mode = "relative"
        units = "%"
        df[phases] = df[phases].div(df[phases].sum(axis=1), axis=0) * 100
    else:
        bar_mode = "stack"

    # Plotly charts (GWP, midpoints, and endpoints)
    if impact_category == "Carbon Footprint":
        fig = px.bar(df, x='System', y=phases, barmode=bar_mode,
                     title="Comparison of Systems")
        fig.update_layout(yaxis_title=units, legend_title=None)
        fig.update_layout(font=dict(family="Arial", size=26, color="black"))

        # Display chart
        col2.plotly_chart(fig)

    elif impact_category == "ReCiPe Endpoint H":
        # fig1 = px.bar(df, x='Midpoint', y=phases, color='System', 
        #               barmode='group', orientation='v',
        #               title="Comparison of Systems")
        fig1 = px.bar(df, x='System', y=phases, barmode=bar_mode,   
                     title="Comparison of Systems (single score)")
        # fig = px.bar(df, y='Midpoint', x=phases, color='System', barmode='group', orientation='h')

        fig2 = px.bar(df[df['System'] == 'Sand Battery'], 
                      x='Midpoint', y=phases, barmode=bar_mode,
                      title="Sand Battery (endpoint breakdown by midpoint categories)")
        fig3 = px.bar(df[df['System'] == 'BESS'], 
                      x='Midpoint', y=phases, barmode=bar_mode, 
                      title="BESS (endpoint breakdown by midpoint categories)")
        fig4 = px.bar(df[df['System'] == 'Propane'], 
                      x='Midpoint', y=phases, barmode=bar_mode,
                      title="Propane (endpoint breakdown by midpoint categories)")
        # Update layout for both charts
        fig1.update_layout(yaxis_title=units, legend_title=None)
        fig1.update_layout(font=dict(family="Arial", size=26, color="black"))
        fig2.update_layout(yaxis_title=units, legend_title=None)
        fig2.update_layout(font=dict(family="Arial", size=26, color="black"))
        fig3.update_layout(yaxis_title=units, legend_title=None)
        fig3.update_layout(font=dict(family="Arial", size=26, color="black"))
        fig4.update_layout(yaxis_title=units, legend_title=None)
        fig4.update_layout(font=dict(family="Arial", size=26, color="black"))

        # Display vertically
        col2.plotly_chart(fig1)
        st.divider # Divider for better visual separation
        col2.plotly_chart(fig2)
        col2.plotly_chart(fig3)
        col2.plotly_chart(fig4)
    else:
        fig = px.bar(df, x='Midpoint', y=phases, barmode=bar_mode,
                     title="Comparison of Systems")
        fig.update_layout(yaxis_title=units, legend_title=None)
        fig.update_layout(font=dict(family="Arial", size=26, color="black"))
        
        # Display chart
        col2.plotly_chart(fig)

    st.divider()
    st.subheader("Selected Options")
    st.write("Impact Method:", impact_category)
    st.write("Outage Frequency:", outage_frequency)