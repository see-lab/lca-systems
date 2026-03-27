# Second tab -- details about the systems/methods
import streamlit as st

def show():
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