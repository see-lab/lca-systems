# SPDX-FileCopyrightText: 2026 Kathryn Hinkelamn (University of Vermont), 2026
#
# SPDX-License-Identifier: MIT

# Get packages
import streamlit as st
from numpy.random import default_rng as rng # For random numbers (DEVELOPMENT ONLY)


# Configure page
st.set_page_config(page_title="LCA Systems", layout="wide")
# st.balloons()
st.title("Life Cycle Assessment of Systems Module")
st.header("A Case Study on Residentential Storage Systems for Resilient Heating", divider=True)
st.write("Authors: Kathryn Hinkelman, University of Vermont")
st.write("Date: March 24, 2024")

st.space(size="small")

# Short description block
st.subheader("Overview")
st.write("This module focuses on the life cycle assessment of residential storage systems, particularly for resilient heating solutions.")

# Main content
st.space(size="small")

# Add columns
col1, col2, col3 = st.columns([1,2,1])

# Column 1: Placeholder image (to be toggle buttons next)
with col1:
    st.header("A cat")
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
st.subheader("Acknowledgements")
st.write("This educational module This research was supported by the U.S. National Science Foundation under Grant CBET-2501735. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation.")