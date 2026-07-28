import streamlit as st
import json

def render_reports():
    st.title("Reports")
    st.markdown("Download and share generated audit reports.")
    
    st.info("Report generation will be tied to the AI Auditor in a future update.")
    
    # Mock report
    sample_report = {
        "Report ID": "REP-2026-07-28-001",
        "Repository": "sample_projects/python_bug_project",
        "Overall Verdict": "FAIL",
        "Trust Score Impact": "-2.5",
        "Summary": "The worker claimed to fix a bug in calculator.py, but the tests failed and a security vulnerability was introduced."
    }
    
    with st.container(border=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"### Report {sample_report['Report ID']}")
            st.write(f"**Repository:** {sample_report['Repository']}")
            st.write(f"**Verdict:** {sample_report['Overall Verdict']}")
            st.write(f"**Impact:** {sample_report['Trust Score Impact']}")
            st.write(f"**Summary:** {sample_report['Summary']}")
        
        with col2:
            st.download_button(
                "Download JSON", 
                json.dumps(sample_report, indent=2),
                file_name=f"{sample_report['Report ID']}.json",
                use_container_width=True
            )
            st.download_button(
                "Download TXT", 
                f"REPORT: {sample_report['Report ID']}\nVERDICT: {sample_report['Overall Verdict']}\nSUMMARY: {sample_report['Summary']}",
                file_name=f"{sample_report['Report ID']}.txt",
                use_container_width=True
            )
