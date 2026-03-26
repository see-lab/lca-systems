# SPDX-FileCopyrightText: 2026 Kathryn Hinkelamn (University of Vermont), 2026
#
# SPDX-License-Identifier: MIT

# Get packages
import streamlit as st
import pandas as pd 
from numpy.random import default_rng as rng # For random numbers (DEVELOPMENT ONLY)
import plotly.express as px

# Configure page
st.set_page_config(page_title="LCA Systems", layout="wide")

st.title("Life Cycle Assessment of Systems Module")
st.header("A Case Study on Residential Storage Systems for Resilient Heating")
st.markdown("**Authors:** Kathryn Hinkelman & Anastasija Mensikova, University of Vermont")
st.markdown("**Date:** March 24, 2024")

# Under construction
st.warning(":building_construction: We are working on this page. Stay tuned.")

################## Define two tabs ####################
tab1, tab2 = st.tabs(["Analysis Tool", "Supporting Details"])

with tab1:
    # Main content
    st.header("Impact Analysis Tool", divider=True)

    # Add columns
    col1, col2 = st.columns([1,4])

    # Column 1: Selection options
    with col1:
        st.subheader("Select Analysis Options")

        impact_category = st.selectbox("Choose an impact method:", 
            ["Carbon Footprint", "ReCiPe Midpoint H", "ReCiPe Endpoint H"])

        impact_location = st.selectbox("Choose a location:", 
            ["Vermont", "Colorado", "California", "Wild Card"])

        st.warning(":building_construction: Add Weighting Factors.")


        st.divider()
        st.subheader("Selected Options")
        st.write("Impact Method:", impact_category)
        st.write("Location:", impact_location)

    # Save the path based on impact category selected.
    PATH = f"./data/GWP100.csv" # MODIFY
    df = pd.read_csv(PATH)

    # Plot the charts
    phases = ["Materials & Mfg", "Transport", "Use", "End-of-Life"]
    units = "kg CO2e" if impact_category == "Carbon Footprint" else "Points"
    col2.subheader(f"{impact_category}")

    # Plotly chart
    fig = px.bar(df, x='System', y=phases)
    fig.update_layout(yaxis_title=units, legend_title=None)
    fig.update_layout(
        font=dict(
            family="Arial",
            size=26, 
            color="black"
        )
    )
    col2.plotly_chart(fig)
    # col2.bar_chart(df, x="System", y=phases, horizontal=False)

    # Display data based on selected system(s). Get the system from the first column of the data frame and filter based on the selected systems.
    # df = df[df["System"].isin(systems)]

    # col2.subheader("A wide column with the charts")
    # col2.line_chart(df)

    # col3.subheader("A narrow column with the data")
    # col3.write(df)

with tab2:
    # Short description block
    st.header("Overview", divider=True)

    # Add columns
    col1, col2 = st.columns([2,1])

    # Text description
    with col1:
        st.markdown("### Problem Set Up")
        st.markdown('''This module focuses on the life cycle assessment of residential 
                    storage systems, particularly for resilient heating solutions.
                    The goal is to compare two alternative storage technologies: (1) a battery-based (Li-ion) system and 
                    (2) a thermal storage system (silica sand, i.e., a sand battery).
                    ''')
        st.markdown("- **Goal:** Estimate biggest impacts to set design priorities.")
        st.markdown("- **Functional Unit:** 200 kWh energy stored with a 15-year lifetime (3-day-long outages, 6 outages/year).")
        st.markdown("- **System Boundary:** Scope 3 cradle-to-grave (materials & mfg, transport, & end of life).")
        st.markdown("- **Impact Units:** Several options (see drop down below).")
        st.markdown("### Questions to Consider")
        st.markdown("This tool analyzes the environmental impacts from each system under various impact scenarios and locations to understand:")
        st.markdown("- How does environmental impact methods change the perception of each alternate's performance?")
        st.markdown("- What are the key impact drivers for each system?")
        st.markdown("- How do the results vary across different locations (e.g., due to differences in electricity grid mix)?")
        st.markdown("- How do the results inform design priorities for improving the sustainability of these systems?")

    # System boundary image
    with col2:
        st.image("img/placeholder.png", caption="System boundaries (a) and (b).")
        # Add dog image
        # st.image("https://static.streamlit.io/examples/dog.jpg")

    # Acknowledgements
    st.subheader("Acknowledgements", divider=True)
    st.write('''The development of this educational module was supported by the U.S. 
            National Science Foundation under Grant CBET-2501735. Any opinions, f
            indings, and conclusions or recommendations expressed in this material 
            are those of the authors and do not necessarily reflect the views of the 
            National Science Foundation.''')

