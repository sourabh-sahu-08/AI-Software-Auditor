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
from frontend.audit_reports import render_audit_reports
from frontend.trust_score import render_trust_score
from frontend.settings import render_settings

def main():
    """
    Main application function that handles the sidebar navigation and page routing.
    """
    st.sidebar.title("Navigation")
    
    # Define navigation options
    nav_options = [
        "Dashboard", 
        "GitHub Issues", 
        "Audit Reports", 
        "Trust Score", 
        "Settings"
    ]
    
    # Sidebar navigation selection
    selected_page = st.sidebar.radio("Go to", nav_options)
    
    # Route to the appropriate page function based on selection
    if selected_page == "Dashboard":
        render_dashboard()
    elif selected_page == "GitHub Issues":
        render_github_issues()
    elif selected_page == "Audit Reports":
        render_audit_reports()
    elif selected_page == "Trust Score":
        render_trust_score()
    elif selected_page == "Settings":
        render_settings()

if __name__ == "__main__":
    main()
