# First tab -- main app

# Import
import streamlit as st
import pandas as pd 
import plotly.express as px
from plotly.subplots import make_subplots as sp

def show():
    # Main content with progress indicator
    col_header1, col_header2 = st.columns([3, 1])
    
    with col_header1:
        st.header("🔬 Impact Analysis Tool", divider=True)

        # Add learning objectives
        with st.expander("📚 Learning Objectives", expanded=False):
            st.markdown("""
            **After using this tool, you will be able to:**
            - Analyze and compare multi-category LCIA outputs for alternative technologies.
            - Evaluate LCIA results for systems engineering decisions, considering modeling limitations and subsequential areas for analysis.
            - Determine the extent to which assumptions and uncertainty influence comparative technology rankings. 
            - Justify whether conclusions are robust or dependent on methodological choices.
            """)
    
    with col_header2:
        # Initialize session state for tracking exploration
        if 'explorations' not in st.session_state:
            st.session_state.explorations = set()
        
        # Show exploration counter
        explored = len(st.session_state.explorations)
        progress = min(explored / 10, 1.0)
        
        st.metric("🎯 Exploration Progress", 
                 f"{min(explored, 10)}/10", 
                 f"{progress*100:.0f}% Complete")
        
        if progress >= 1.0:
            st.success("🏆 Expert Explorer!")


    # Add columns
    col1, col2 = st.columns([1,4])

    # Column 1: Selection options
    with col1:
        st.subheader("🎯 Select Analysis Options")

        impact_category = st.selectbox("🔬 Choose an impact method:", 
            ["Carbon Footprint", "ReCiPe Endpoint H", "ReCiPe Midpoint H"],
            help="Different methods capture different environmental concerns. Start with Carbon Footprint for climate impacts!")

        outage_frequency = st.selectbox("⚡ Choose an outage frequency scenario:", 
            ["Rare (5x/year)", "Moderate outages (10x/yr)", "Frequent outages (20x/yr)", "Regular heating use (85x/yr)"],
            index=1,
            help="How often will the storage system be used? This affects the 'Use' phase impacts.")

        relative_results = st.checkbox("📊 Scale plots to relative values?", value=False,
                                     help="Convert to percentages for easier comparison across impact categories with different units.")
        
        # Add interactive tip
        if not relative_results and impact_category == "ReCiPe Midpoint H":
            st.info("💡 **Tip**: Try enabling relative scaling when comparing midpoint categories!")

        # Add quick insights section
        with st.expander("🧠 Quick Insights", expanded=False):
            if impact_category == "Carbon Footprint":
                st.write("🌍 **Focus**: Climate change impacts from greenhouse gas emissions")
                st.write(" * **Problem**-level")
                st.write(" * **Single** impact category")
            elif impact_category == "ReCiPe Endpoint H":
                st.write("🎯 **Focus**: Single-score environmental impacts")
                st.write(" * **Damage**-level")
                st.write(" * **Multiple** impact categories")           
            else:
                st.write("🔍 **Focus**: Detailed breakdown of specific environmental impact types")
                st.write(" * **Problem**-level")
                st.write(" * **Multiple** impact categories") 

    # Save the path based on impact category selected.
    if impact_category == "Carbon Footprint":
        PATH = f"./data/GWP100.csv"
    elif impact_category == "ReCiPe Midpoint H":
        PATH = f"./data/ReCiPe-Midpoint.csv"
    else:
        PATH = f"./data/ReCiPe-Endpoint.csv"
    df = pd.read_csv(PATH)  # Save data frame from assigned path

    # Track exploration progress
    current_selection = f"{impact_category}_{outage_frequency}_{relative_results}"
    if 'explorations' not in st.session_state:
        st.session_state.explorations = set()
    st.session_state.explorations.add(current_selection)

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
    elif outage_frequency == "Frequent outages (20x/yr)":
        df = df[df['Outage'] == 'Frequent']
    else:
        df = df[df['Outage'] == 'Regular']
    
    # Save separate dataframe for endpoints that sum all midpoints down to one score for each system
    # Sum all midpoint categories for each system to get single endpoint scores
    df_endpoint = df.groupby('System')[phases].sum().reset_index()

    #  Modifications if relative results is selected
    if relative_results:
        bar_mode = "relative"
        units = "%"
        df[phases] = df[phases].div(df[phases].sum(axis=1), axis=0) * 100
        df_endpoint[phases] = df_endpoint[phases].div(df_endpoint[phases].sum(axis=1), axis=0) * 100
    else:
        bar_mode = "stack"

    ######## Plotly charts (GWP, midpoints, and endpoints)
    
    ### CARBON FOOTPRINT RESULTS
    if impact_category == "Carbon Footprint":
        fig = px.bar(df, x='System', y=phases, barmode=bar_mode,
                     title="🌍 Carbon Footprint Comparison",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(
            yaxis_title=units, 
            legend_title="Lifecycle Phases",
            font=dict(family="Arial", size=14, color="black"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        # Add hover information
        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>" +
                         "Phase: %{fullData.name}<br>" +
                         "Impact: %{y:.2f} " + units + "<br>" +
                         "<extra></extra>"
        )

        # Display chart
        col2.plotly_chart(fig, use_container_width=True)
        
        # Add quick insights below chart
        col2_1, col2_2, col2_3 = col2.columns(3)
        
        # Calculate which system is best
        total_impacts = df.groupby('System')[phases].sum().sum(axis=1)
        best_system = total_impacts.idxmin()
        worst_system = total_impacts.idxmax()
        
        with col2_1:
            st.metric("🏆 Best System", best_system, 
                     f"{total_impacts[best_system]:.0f} {units}")
        with col2_2:
            st.metric("📈 Highest Impact", worst_system,
                     f"{total_impacts[worst_system]:.0f} {units}")
        with col2_3:
            # Calculate dominant phase
            phase_totals = df[phases].sum()
            dominant_phase = phase_totals.idxmax()
            st.metric("🔍 Key Phase", dominant_phase,
                     f"{(phase_totals[dominant_phase]/phase_totals.sum()*100):.0f}% of total")

    ### RECIPE ENDPOINT RESULTS
    elif impact_category == "ReCiPe Endpoint H":
        # Plot single score results
        fig1 = px.bar(df_endpoint, x='System', y=phases, barmode=bar_mode,
                     title="🎯 ReCiPe Endpoint Comparison (Single Score)",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig1.update_layout(
            yaxis_title=units, 
            legend_title="Lifecycle Phases",
            font=dict(family="Arial", size=14, color="black"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig1.update_traces(
            hovertemplate="<b>%{x}</b><br>" +
                         "Phase: %{fullData.name}<br>" +
                         "Impact: %{y:.2f} " + units + "<br>" +
                         "<extra></extra>"
        )
        
        # Plot midpoint results for each system
        fig2 = px.bar(df[df['System'] == 'Sand Battery'], 
                      x='Midpoint', y=phases, barmode=bar_mode,
                      title="🏖️ Sand Battery (Breakdown by Impact Categories)",
                      color_discrete_sequence=px.colors.qualitative.Set2)
        fig2.update_layout(
            yaxis_title=units, 
            legend_title="Lifecycle Phases",
            font=dict(family="Arial", size=14, color="black"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig2.update_traces(
            hovertemplate="<b>%{x}</b><br>" +
                         "Phase: %{fullData.name}<br>" +
                         "Impact: %{y:.2f} " + units + "<br>" +
                         "<extra></extra>"
        )
        fig2.update_xaxes(tickangle=45)
        
        fig3 = px.bar(df[df['System'] == 'BESS'], 
                      x='Midpoint', y=phases, barmode=bar_mode, 
                      title="🔋 BESS (Breakdown by Impact Categories)",
                      color_discrete_sequence=px.colors.qualitative.Set2)
        fig3.update_layout(
            yaxis_title=units, 
            legend_title="Lifecycle Phases",
            font=dict(family="Arial", size=14, color="black"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig3.update_traces(
            hovertemplate="<b>%{x}</b><br>" +
                         "Phase: %{fullData.name}<br>" +
                         "Impact: %{y:.2f} " + units + "<br>" +
                         "<extra></extra>"
        )
        fig3.update_xaxes(tickangle=45)
        
        fig4 = px.bar(df[df['System'] == 'Propane'], 
                      x='Midpoint', y=phases, barmode=bar_mode,
                      title="🔥 Propane (Breakdown by Impact Categories)",
                      color_discrete_sequence=px.colors.qualitative.Set2)
        fig4.update_layout(
            yaxis_title=units, 
            legend_title="Lifecycle Phases",
            font=dict(family="Arial", size=14, color="black"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig4.update_traces(
            hovertemplate="<b>%{x}</b><br>" +
                         "Phase: %{fullData.name}<br>" +
                         "Impact: %{y:.2f} " + units + "<br>" +
                         "<extra></extra>"
        )
        fig4.update_xaxes(tickangle=45)

        # Display vertically
        col2.plotly_chart(fig1, use_container_width=True)
        
        # Add quick insights below main chart
        col2_1, col2_2, col2_3 = col2.columns(3)
        
        # Calculate which system is best for endpoint
        total_impacts = df_endpoint.groupby('System')[phases].sum().sum(axis=1)
        best_system = total_impacts.idxmin()
        worst_system = total_impacts.idxmax()
        
        with col2_1:
            st.metric("🏆 Best System", best_system, 
                     f"{total_impacts[best_system]:.0f} {units}")
        with col2_2:
            st.metric("📈 Highest Impact", worst_system,
                     f"{total_impacts[worst_system]:.0f} {units}")
        with col2_3:
            # Calculate dominant phase for endpoint
            phase_totals = df_endpoint[phases].sum()
            dominant_phase = phase_totals.idxmax()
            st.metric("🔍 Key Phase (all systems)", dominant_phase,
                     f"{(phase_totals[dominant_phase]/phase_totals.sum()*100):.0f}% of total")
        
        col2.divider() # Divider for better visual separation
        col2.plotly_chart(fig2, use_container_width=True)
        col2.plotly_chart(fig3, use_container_width=True)
        col2.plotly_chart(fig4, use_container_width=True)

    ### RECIPE MIDPOINT RESULTS
    else:
        # Select a midpoint category
        with col2:
            midpoint_category = st.selectbox("🔍 Select a midpoint category to display:", midpoints, index=0,
                                           help="Each midpoint represents a specific environmental impact type")

        # Filter the data to only show bar charts for the selected midpoint category
        df_midpoint = df[df['Midpoint'] == midpoint_category]
        # Set units based on the selection
        units_midpoint = df_midpoint['Unit'].iloc[0] if not relative_results else "%"
        
        # Plot bar charts for all three systems for the selected midpoint category
        fig = px.bar(df_midpoint, x='System', y=phases, barmode=bar_mode,
                     title=f"🔬 {midpoint_category} Comparison",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(
            yaxis_title=units_midpoint, 
            legend_title="Lifecycle Phases",
            font=dict(family="Arial", size=14, color="black"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>" +
                         "Phase: %{fullData.name}<br>" +
                         "Impact: %{y:.2f} " + units_midpoint + "<br>" +
                         "<extra></extra>"
        )

        # Display chart
        col2.plotly_chart(fig, use_container_width=True)
        
        # Add quick insights below chart for midpoint
        col2_1, col2_2, col2_3 = col2.columns(3)
        
        # Calculate which system is best for this midpoint
        total_impacts = df_midpoint.groupby('System')[phases].sum().sum(axis=1)
        best_system = total_impacts.idxmin()
        worst_system = total_impacts.idxmax()
        
        with col2_1:
            st.metric("🏆 Best System", best_system, 
                     f"{total_impacts[best_system]:.2f} {units_midpoint}")
        with col2_2:
            st.metric("📈 Highest Impact", worst_system,
                     f"{total_impacts[worst_system]:.2f} {units_midpoint}")
        with col2_3:
            # Calculate dominant phase for this midpoint
            phase_totals = df_midpoint[phases].sum()
            dominant_phase = phase_totals.idxmax()
            st.metric("🔍 Key Phase", dominant_phase,
                     f"{(phase_totals[dominant_phase]/phase_totals.sum()*100):.0f}% of total")
        # st.divider() # Divider for better visual separation
        # Add all data for each system as a table
        # col2.subheader(f"Data for all midpoints and all systems")
        # Save a df_display that has "System" as the index and removes the "Outage" column
        # df_display = df.drop(columns=['Outage']).set_index('System')
        # col2.table(df_display)

    st.divider()
    
    # Enhanced results section with interpretation
    col_results1, col_results2 = st.columns([2, 1])
    
    with col_results1:
        st.subheader("📋 Analysis Summary")
        st.write("**Impact Method:** ", impact_category)
        st.write("**Outage Scenario:** ", outage_frequency)
        st.write("**Display Mode:** ", "Relative (%)" if relative_results else "Absolute Values")
    
    with col_results2:
        st.subheader("🤔 Discussion Questions")
        with st.expander("Think About This...", expanded=False):
            st.markdown("""
            - Which system performs best for this impact method?
            - Which lifecycle phase has the largest impact?
            - How do your results change with different scenarios?
            - What design improvements would you recommend?
            """)
    
    # Add interpretation based on current selection
    st.subheader("🔍 What Do These Results Mean?")
    
    if impact_category == "Carbon Footprint":
        st.info("""
        **Climate Impact Perspective**: Lower values = better for climate change.
        The 'Materials & Mfg' phase often dominates for batteries due to energy-intensive production.
        The 'Use' phase varies greatly depending on how clean the electricity grid is.
        """)
    elif impact_category == "ReCiPe Endpoint H":
        st.info("""
        **Comprehensive Environmental View**: This combines multiple impact types into single scores.
        Look at both the overall comparison AND the breakdown by impact categories.
        Different systems may excel in different environmental areas.
        Consider enabling relative scaling to see details within each impact category.
        """)
    else:
        st.info("""
        **Detailed Impact Analysis**: Each midpoint category represents a specific environmental concern (i.e., problem).
        Use this to identify which environmental impacts matter most for each system.
        Consider enabling relative scaling to compare across different impact types.
        """)
        
    # Add interactive challenge
    st.subheader("🎯 Try This Challenge!")
    challenge_options = [
        "Complete the comparative analysis table for moderate outage scenario",
        "Rank the top 3 midpoint categories for each system using ReCiPe Endpoint",
        "Explore how outage frequency affects system rankings",
        "Compare system performance across different impact methods",
        "Determine when the 'Use' phase becomes significant"
    ]
    selected_challenge = st.selectbox("Pick a challenge to explore:", 
                                    ["Select a challenge..."] + challenge_options)
    
    if selected_challenge != "Select a challenge...":
        st.success(f"🚀 **Challenge**: {selected_challenge}")
        st.markdown("*Use the controls above to explore and find your answer!*")