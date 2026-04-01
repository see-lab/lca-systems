# SPDX-FileCopyrightText: 2026 Kathryn Hinkelamn (University of Vermont), 2026
#
# SPDX-License-Identifier: MIT

# Get packages
import streamlit as st

# Configure page
st.set_page_config(
    page_title="LCIA Systems Workshop", 
    layout="wide",
    page_icon="🌍",
    initial_sidebar_state="expanded"
)

# Add workshop header
col_title1, col_title2 = st.columns([3, 1])

with col_title1:
    st.title("🌍 Life Cycle Impact Assessment of Systems")
    st.header("⚡ Residential Storage Systems for Resilient Heating")
    st.markdown("**👥 Authors:** Kathryn Hinkelman & Anastasija Mensikova, University of Vermont")
    st.markdown("**📅 Version 1.0 alpha:** April 2, 2026")

with col_title2:
    # Workshop timer/progress
    if 'workshop_start_time' not in st.session_state:
        import time
        st.session_state.workshop_start_time = time.time()
    
    # Calculate elapsed time
    import time
    elapsed = time.time() - st.session_state.workshop_start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    
    st.metric("⏱️ Workshop Time", f"{minutes:02d}:{seconds:02d}")
    
    # Add workshop mode toggle
    workshop_mode = st.toggle("🎓 Workshop Mode", value=True)

# Workshop instructions
if workshop_mode:
    st.info("""
    🎯 **Workshop Instructions**: 
    1. Start with the **Analysis Tool** tab to explore different scenarios
    2. Use **Supporting Details** to understand the systems and methodology  
    3. Complete the in-class **worksheet** to guide your exploration and analysis
    4. Discuss findings with your team members!
    """)

# Remove construction warning for workshop mode
if not workshop_mode:
    st.info('''Thank you for visiting our LCA Systems Module! 
             We are currently developing and refining the content. 
             Please check back soon for updates and new features. 
             In the meantime, feel free to explore 
             the existing content and provide feedback!''')


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