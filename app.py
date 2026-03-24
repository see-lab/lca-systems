# SPDX-FileCopyrightText: 2026 Kathryn Hinkelamn (University of Vermont), 2026
#
# SPDX-License-Identifier: MIT

# Get packages
import streamlit as st
from numpy.random import default_rng as rng # For random numbers (DEVELOPMENT ONLY)


# Configure page
st.set_page_config(page_title="LCA Systems", layout="wide")

st.title("Life Cycle Assessment of Systems Module")
st.header("A Case Study on Residentential Storage Systems for Resilient Heating")
st.markdown("**Authors:** Kathryn Hinkelman, University of Vermont")
st.markdown("**Date:** March 24, 2024")


st.space(size="small")

# Short description block
st.header("Problem Set Up", divider=True)

# Add columns
col1, col2 = st.columns([2,1])

# Text description
with col1:
    st.markdown('''This module focuses on the life cycle assessment of residential 
                storage systems, particularly for resilient heating solutions.
                The goal is to compare two alternative storage technologies: (1) a battery-based (Li-ion) system and 
                (2) a thermal storage system (silica sand, i.e., a sand battery).
                ''')
    st.markdown("- **Goal:** Estimate biggest impacts to set design priorities.")
    st.markdown("- **Functional Unit:** 200 kWh of energy storage for residential heating over a 3-day outage and a 15-year lifetime.")
    st.markdown("- **System Boundary:** Scope 3 cradle-to-grave (materials & mfg, transport, & end of life).")
    st.markdown("- **Impact Units:** Several options (see drop down below).")
    st.markdown("## Learning Objectives")
    st.markdown("The analysis will consider the environmental impacts associated with each system under various impact scenarios to understand:")
    st.markdown("- Which system has the lowest environmental impact under different impact categories?")
    st.markdown("- What are the key drivers of impact for each system?")
    st.markdown("- How do the results inform design priorities for improving the sustainability of these systems?")

# System boundary image
with col2:
    st.image("img/placeholder.png", caption="System boundaries (a) and (b).")

# Main content
st.space(size="small")

st.header("Impact Analysis Tool", divider=True)

# Add columns
col1, col2, col3 = st.columns([1,2,1])

# Column 1: Placeholder image (to be toggle buttons next)
with col1:
    st.subheader("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg")

# Random data for testing charts
df = rng(0).standard_normal((10, 1))

col2.subheader("A wide column with a chart")
col2.line_chart(df)

col3.subheader("A narrow column with the data")
col3.write(df)

#### NOT USED
# Under construction
# st.warning(":building_construction: We are working on this page. Stay tuned.")

# Acknowledgements
st.subheader("Acknowledgements", divider=True)
st.write("The development of this educational module was supported by the U.S. National Science Foundation under Grant CBET-2501735. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation.")