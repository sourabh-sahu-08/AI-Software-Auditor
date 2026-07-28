import streamlit as st
import json

def render_worker_analysis():
    st.title("Worker Analysis")
    st.markdown("Detailed breakdown of AI Worker analysis for GitHub issues.")
    
    if "ai_analysis" not in st.session_state or not st.session_state["ai_analysis"]:
        st.info("No AI analyses have been run yet. Go to **GitHub Issues**, select an issue, and click **Analyze with AI**.")
        return
        
    analysis_dict = st.session_state["ai_analysis"]
    
    # Create a dropdown to select which analysis to view
    options = [f"#{num} - {data['title']}" for num, data in analysis_dict.items()]
    selected_option = st.selectbox("Select an analyzed issue", options)
    
    if selected_option:
        issue_num = int(selected_option.split(" - ")[0].replace("#", ""))
        record = analysis_dict[issue_num]
        analysis_data = record["data"]
        response_time = record["time"]
        
        st.markdown("---")
        
        # Action Buttons
        col_btn1, col_btn2 = st.columns([1, 10])
        with col_btn1:
            json_str = json.dumps(analysis_data, indent=2)
            st.download_button("Download JSON", json_str, file_name=f"analysis_{issue_num}.json")
            
        # Metrics Cards
        col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
        with col_metrics1:
            st.metric("🎯 Confidence", f"{analysis_data.get('confidence', 0)}%")
        with col_metrics2:
            st.metric("Claim", analysis_data.get('claim', 'N/A'))
        with col_metrics3:
            st.metric("Response Time", f"{response_time}s")
            
        st.progress(analysis_data.get('confidence', 0) / 100.0, text="Confidence Level")
            
        st.write("")
        
        # Tabs for details
        tab1, tab2, tab3 = st.tabs(["🧠 Root Cause", "🛠 Suggested Fix", "📂 Files To Modify"])
        
        with tab1:
            st.info(analysis_data.get('root_cause', 'No root cause specified.'))
            
        with tab2:
            st.success(analysis_data.get('suggested_fix', 'No fix suggested.'))
            
        with tab3:
            files = analysis_data.get('files_to_modify', [])
            if isinstance(files, list) and files:
                for f in files:
                    st.code(f, language="text")
            else:
                st.write("No files specified.")
                
        with st.expander("Raw AI Output", expanded=False):
            st.json(analysis_data)
