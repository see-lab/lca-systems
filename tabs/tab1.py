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
            ["Carbon Footprint", "ReCiPe Midpoint H", "ReCiPe Endpoint H"])

        outage_frequency = st.selectbox("Choose an outage frequency:", 
            ["Rare (5x/year)", "Moderate outages (10x/yr)", "Frequent outages (20x/yr)"])

        st.warning(":building_construction: Add Weighting Factors.")


    # Save the path based on impact category selected.
    if impact_category == "Carbon Footprint":
        PATH = f"./data/GWP100.csv"
    elif impact_category == "ReCiPe Midpoint H":
        PATH = f"./data/ReCiPe.csv"
    else:
        PATH = f"./data/ReCiPe.csv"
    df = pd.read_csv(PATH)  # Save data frame from assigned path

    # Plot the charts
    phases = ["Materials & Mfg", "Transport", "Use", "End-of-Life"]
    units = "kg CO2e" if impact_category == "Carbon Footprint" else "Points"
    col2.subheader(f"{impact_category}")

    # Plotly chart (one type for midpoints; one for endpoints)
    if impact_category == "ReCiPe Midpoint H":
        fig1 = px.bar(df, x='Midpoint', y=phases, color='System', 
                      barmode='group', orientation='v',
                      title="Comparison of Systems")
        # fig = px.bar(df, y='Midpoint', x=phases, color='System', barmode='group', orientation='h')
        fig2 = px.bar(df[df['System'] == 'Sand Battery'], 
                      x='Midpoint', y=phases,
                      title="Sand Battery Breakdown")
        fig3 = px.bar(df[df['System'] == 'BESS'], 
                      x='Midpoint', y=phases,
                      title="BESS Breakdown")
        # Update layout for both charts
        fig1.update_layout(yaxis_title=units, legend_title=None)
        fig1.update_layout(font=dict(family="Arial", size=26, color="black"))
        fig2.update_layout(yaxis_title=units, legend_title=None)
        fig2.update_layout(font=dict(family="Arial", size=26, color="black"))
        fig3.update_layout(yaxis_title=units, legend_title=None)
        fig3.update_layout(font=dict(family="Arial", size=26, color="black"))

        # Display vertically
        col2.plotly_chart(fig1)
        col2.plotly_chart(fig2)
        col2.plotly_chart(fig3)
    else:
        fig = px.bar(df, x='System', y=phases,
                     title="Comparison of Systems (Single Score)")
        fig.update_layout(yaxis_title=units, legend_title=None)
        fig.update_layout(font=dict(family="Arial", size=26, color="black"))
        
        # Display chart
        col2.plotly_chart(fig)

    st.divider()
    st.subheader("Selected Options")
    st.write("Impact Method:", impact_category)
    st.write("Outage Frequency:", outage_frequency)