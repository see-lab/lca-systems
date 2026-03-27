# First tab -- main app

# Import
import streamlit as st
import pandas as pd 
import plotly.express as px

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