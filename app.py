# SPDX-FileCopyrightText: 2026 Kathryn Hinkelamn (University of Vermont), 2026
#
# SPDX-License-Identifier: MIT

# Get packages
import streamlit as st

# Configure page
st.set_page_config(page_title="LCA Systems", layout="wide")

st.title("Life Cycle Assessment of Systems Module")
st.header("A Case Study on Residential Storage Systems for Resilient Heating")
st.markdown("**Authors:** Kathryn Hinkelman & Anastasija Mensikova, University of Vermont")
st.markdown("**Version 0.1 pre-alpha:** March 25, 2026")

# Under construction
st.warning(":building_construction: We are working on this page. Stay tuned.")


################## Define tabs ####################
from tabs import tab1, tab2, tab3
t1, t2, t3 = st.tabs(["Analysis Tool", "Supporting Details", "Inventory Data"])

with t1:
    tab1.show()

with t2:
    tab2.show()

with t3:
    tab3.show()

# SimaPro project
# Project Name: EnergyStorage
# Structure
# Product stages
    # > "Subs" -- ["Materials & Mfg", "Transport", "Use", "End-of-Life"]
    #             [BESS_Production, BESS_Use, etc.]
    # > [folder name] -- [BESS, Sand, Propane]

# LCIA Running [BESS, Sand, Propane] with various methods

# Create a csv for each system [BESS, Sand, Propane] for inventory
# Stage, Item, Inventory Selection, Inventory UID, Quantity, Unit
# Mgf, Copper, [long name], ####, 100, kg