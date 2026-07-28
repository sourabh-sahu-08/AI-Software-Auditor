"""
Main entry point for the AI Software Auditor Streamlit application.
Sets up the frontend and initializes the application.
"""
import streamlit as st

# Configure the Streamlit page settings (must be the first Streamlit command)
st.set_page_config(
    page_title="AI Software Auditor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import frontend modules
from frontend.dashboard import render_dashboard
from frontend.github_issues import render_github_issues
from frontend.worker_analysis import render_worker_analysis
from frontend.verification import render_verification
from frontend.audit_reports import render_audit_reports
from frontend.trust_score import render_trust_score
from frontend.analytics import render_analytics
from frontend.settings import render_settings
from frontend.reports import render_reports

def main():
    """
    Main application function that handles the sidebar navigation and page routing.
    """
    st.sidebar.title("Navigation")
    
    # Define navigation options based on the enterprise spec
    nav_options = [
        "Dashboard", 
        "GitHub Issues", 
        "Worker Analysis",
        "Verification",
        "Audit Reports", 
        "Trust Score", 
        "Analytics",
        "Settings",
        "About"
    ]
    
    # Sidebar navigation selection
    selected_page = st.sidebar.radio("Go to", nav_options)
    
    # Route to the appropriate page function based on selection
    if selected_page == "Dashboard":
        render_dashboard()
    elif selected_page == "GitHub Issues":
        render_github_issues()
    elif selected_page == "Worker Analysis":
        render_worker_analysis()
    elif selected_page == "Verification":
        render_verification()
    elif selected_page == "Audit Reports":
        render_audit_reports()
    elif selected_page == "Trust Score":
        render_trust_score()
    elif selected_page == "Analytics":
        render_analytics()
    elif selected_page == "Settings":
        render_settings()
    elif selected_page == "About":
        st.title("About AI Software Auditor")
        st.write("An enterprise-grade platform to monitor AI software engineers and verify their claims objectively.")
        st.write("Current version: 2.0.0")

if __name__ == "__main__":
    main()
