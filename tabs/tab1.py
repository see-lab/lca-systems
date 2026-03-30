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
        PATH = f"./data/ReCiPe-Midpoint.csv"
    else:
        PATH = f"./data/ReCiPe-Endpoint.csv"
    df = pd.read_csv(PATH)  # Save data frame from assigned path

    # Plot the charts
    phases = ["Materials & Mfg", "Transport", "Use", "End-of-Life"]
    midpoints = pd.read_csv("./data/Midpoints.csv")['Midpoint'].tolist()
    units = "kg CO2e" if impact_category == "Carbon Footprint" else "Points"
    col2.subheader(f"{impact_category}")

    # Reduce df based on outage scenario selected
    if outage_frequency == "Rare (5x/year)":
        df = df[df['Outage'] == 'Rare']
    elif outage_frequency == "Moderate outages (10x/yr)":
        df = df[df['Outage'] == 'Moderate']
    else:        
        df = df[df['Outage'] == 'Frequent']
    
    # Save separate dataframe for endpoints that sum all midpoints down to one score for each system
    # Sum all midpoint categories for each system to get single endpoint scores
    df_endpoint = df.groupby('System')[phases].sum().reset_index()
    print("Endpoint scores (sum of all midpoints by system):")
    print(df_endpoint)

    #  Modifications if relative results is selected
    if relative_results:
        bar_mode = "relative"
        units = "%"
        df[phases] = df[phases].div(df[phases].sum(axis=1), axis=0) * 100
        df_endpoint[phases] = df_endpoint[phases].div(df_endpoint[phases].sum(axis=1), axis=0) * 100
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
        # Plot single score results
        fig1 = px.bar(df_endpoint, x='System', y=phases, barmode=bar_mode,
                     title="Comparison of Systems (single score)")
        
        # Plot midpoint results for each system
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
        # Select a midpoint category
        with col2:
            midpoint_category = st.selectbox("Select a midpoint category to display:", midpoints, index=0)

        # Filter the data to only show bar charts for the selected midpoint category
        df_midpoint = df[df['Midpoint'] == midpoint_category]
        # Set units based on the selection
        units = df_midpoint['Unit'].iloc[0]
        # Plot bar charts for all three systems for the selected midpoint category
        fig = px.bar(df_midpoint, x='System', y=phases, barmode=bar_mode,
                     title="Comparison of Systems")
        fig.update_layout(yaxis_title= "%" if relative_results else units, legend_title=None)
        fig.update_layout(font=dict(family="Arial", size=26, color="black"))

        # Display chart
        col2.plotly_chart(fig)
        st.divider() # Divider for better visual separation
        # Add all data for each system as a table
        col2.subheader(f"Data for all midpoints and all systems")
        # Save a df_display that has "System" as the index and removes the "Outage" column
        df_display = df.drop(columns=['Outage']).set_index('System')
        col2.table(df_display)

    st.divider()
    st.subheader("Selected Options")
    st.write("Impact Method:", impact_category)
    st.write("Outage Frequency:", outage_frequency)