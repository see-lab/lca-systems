# Second tab -- details about the systems/methods
import streamlit as st

def show():
    # Short description block
    st.header("🌍 Overview", divider=True)

    # Add columns
    col1, col2 = st.columns([2,1])

    # Text description
    with col1:
        st.markdown("### 🎯 Problem Set Up")
        st.markdown('''This module focuses on the life cycle assessment of residential 
                    energy storage systems, particularly for resilient heating solutions.
                    The goal is to compare three alternative storage technologies -- (1) battery energy storage system (BESS), 
                    (2) a thermal storage system (silica sand, i.e., a "sand battery"), and (3) a propane-based system -- 
                    from a environmental perspective.
                    ''')
        
        st.markdown("### ⚠️ Disclaimer!")
        st.warning("""This module is designed for **educational purposes** to 
                   illustrate how LCA results can inform engineering design decisions.
                   While care has been taken to ensure data accuracy, the results are 
                   based on simplified models and assumptions, which do not capture the full complexity
                   and usage scenarios of real-world energy storage systems and applications.
                   These results are not intended to be used for commercial, policy, or engineering technology 
                   decisions without further analysis and validation.
                   """)
        
        # Interactive elements
        st.markdown("#### 🔑 Key Study Parameters")
        
        col1a, col1b = st.columns(2)
        
        with col1a:
            st.info("""
            **🎯 Goal:** Estimate biggest impacts to set design priorities
            
            **⚖️ Functional Unit:** 200 kWh energy discharged from storage during use over a 15-year lifetime
            
            **🔄 System Boundary:** Cradle-to-grave analysis, including transport (to Vermont)
            """)
            
        with col1b:
            st.success("""
            **📋 Software & Data:** SimaPro 9.3, Ecoinvent 3.9
            
            **📊 Impact Methods:** Multiple environmental indicators
            
            **⚡ Scenarios:** Variable outage frequencies
            
            **🎛️ Analysis:** Absolute & relative comparisons
            """)
        

    with col2:        
        # Add system comparison table
        st.markdown("#### ⚖️ System Comparison")
        
        comparison_data = {
            "Feature": ["Energy Type", "Storage Medium", "Efficiency", "Scalability"],
            "BESS": ["Electrochemical", "Lithium Batteries", "~85-95%", "Modular"],
            "Sand Battery": ["Thermal", "Silica Sand", "~50-70%", "Flexible"],
            "Propane": ["Chemical", "Propane Gas", "~80-90%", "Tank-based"]
        }
        
        st.table(comparison_data)
        
        # Interactive system selector
        st.markdown("#### 🔍 Learn More About Systems")
        
        selected_system = st.selectbox(
            "Select a system to explore:",
            ["Choose a system...", "BESS", "Sand Battery", "Propane"]
        )
        
        system_details = {
            "BESS": {
                "icon": "🔋",
                "description": "Electrochemical energy storage using lithium-ion batteries",
                "pros": ["High efficiency", "Fast response", "Mature technology"],
                "cons": ["Fire safety risk", "Resource intensive", "High capital costs"]
            },
            "Sand Battery": {
                "icon": "🏖️",
                "description": "Thermal energy storage using heated sand as storage medium",
                "pros": ["Long lifespan", "Abundant materials", "Low maintenance"],
                "cons": ["Lower efficiency", "Large footprint", "Novel technology"]
            },
            "Propane": {
                "icon": "🔥",
                "description": "Chemical energy storage using propane combustion for heating",
                "pros": ["High energy density", "Reliable technology", "Quick deployment"],
                "cons": ["Direct emissions", "Fossil fuel & supply dependence", "High usage costs"]
            }
        }
        
        if selected_system in system_details:
            details = system_details[selected_system]
            st.markdown(f"**{details['icon']} {selected_system}**")
            st.write(details["description"])
            
            col_pros, col_cons = st.columns(2)
            with col_pros:
                st.markdown("**✅ Advantages:**")
                for pro in details["pros"]:
                    st.write(f"• {pro}")
            
            with col_cons:
                st.markdown("**⚠️ Challenges:**")
                for con in details["cons"]:
                    st.write(f"• {con}")


    # Add system boundaries
    st.subheader("🏗️ System Boundary Schematics")
    st.write('''Here's schematics to give a picture of what equipment
                 and assumptions are included in the scope. The charging of
                 both the BESS and sand battery are assumed "free" from renewable
                 sources, while the propane comes at a cost.
                 The systems are sized and designed to deliver the same functional unit.''')
    col3a, col3b, col3c = st.columns(3)
    with col3a:
        st.image("img/bess.png", caption="BESS")
    with col3b:
        st.image("img/propane.png", caption="Propane")
    with col3c:
        st.image("img/sand.png", caption="Sand Battery")

    # Enhanced acknowledgements with interactive elements
    st.subheader("🙏 Acknowledgements & Resources", divider=True)
    
    col_ack1, col_ack2 = st.columns([2, 1])
    
    with col_ack1:
        st.write('''**Funding:** The development of this educational module was supported by the U.S. 
                National Science Foundation under Grant CBET-2501735. Any opinions, 
                findings, and conclusions or recommendations expressed in this material 
                are those of the authors and do not necessarily reflect the views of the 
                National Science Foundation.''')
        
        st.write('''**AI Statement:** The design of this interactive educational module 
                was enhanced with assistance from AI tools (Claude Sonnet 4) for code development, user interface design, 
                and documentation. All educational content, data analysis, and LCA processes were
                conceptualized, performed, and validated by the human authors.''')
        
        # Add learning resources
        st.markdown("#### 📚 Additional Learning Resources")
        
        resources = [
            ("📖 ISO 14040 LCA Principles", "https://www.iso.org/standard/37456.html"),
            ("📊 ReCiPe Methodology", "https://www.rivm.nl/en/life-cycle-assessment-lca/recipe"),
            ("📊 IPCC GWP Methodology", "https://www.ipcc.ch/report/ar6/wg3/"),
            ("🎓 LCA Resources", "https://venturewell.org/tools_for_design/measuring-sustainability/life-cycle-assessment-content/"),
            ("⚡ Energy Storage Technologies", "https://eta.lbl.gov/storage"),
            ("🏖 Sand Batteries in Action", "https://polarnightenergy.com/news/what-is-thermal-energy-storage/")
        ]
        
        for title, url in resources:
            st.markdown(f"[{title}]({url})")
    
    with col_ack2:
        # Add interactive feedback form
        st.markdown("#### 💬 Feedback")
        
        with st.form("feedback_form"):
            rating = st.slider("How helpful is this tool?", 1, 5, 3)
            feedback = st.text_area("Suggestions for improvement:")
            submitted = st.form_submit_button("Submit Feedback")
            
            if submitted:
                # Save feedback to a file
                import datetime
                import os
                
                # Create feedback directory if it doesn't exist
                feedback_dir = "feedback"
                if not os.path.exists(feedback_dir):
                    os.makedirs(feedback_dir)
                
                # Create feedback entry with timestamp
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                feedback_entry = f"Timestamp: {timestamp}\nRating: {rating}/5\nFeedback: {feedback}\n{'='*50}\n\n"
                
                # Append to feedback file
                feedback_file = os.path.join(feedback_dir, "user_feedback.txt")
                try:
                    with open(feedback_file, "a", encoding="utf-8") as f:
                        f.write(feedback_entry)
                    st.success("Thank you for your feedback! 🎉 Your response has been saved.")
                except Exception as e:
                    st.success("Thank you for your feedback! 🎉")
                    st.error(f"Note: Could not save to file ({str(e)})")
                
                if rating >= 4:
                    st.balloons()
