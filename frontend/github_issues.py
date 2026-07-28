import streamlit as st
import pandas as pd
from backend.github_service import fetch_open_issues

def render_github_issues():
    """
    Renders the GitHub Issues page, allowing users to fetch and view
    open issues for a given repository.
    """
    st.title("GitHub Issues")
    st.markdown("Fetch and analyze open issues from any GitHub repository.")
    
    # Input fields for Owner and Repository
    col1, col2 = st.columns(2)
    with col1:
        owner = st.text_input("Repository Owner", placeholder="e.g., streamlit")
    with col2:
        repo = st.text_input("Repository Name", placeholder="e.g., streamlit")
        
    fetch_btn = st.button("Fetch Issues", type="primary")
    
    st.markdown("---")
    
    # Initialize session state for issues if not present
    if "github_issues_data" not in st.session_state:
        st.session_state["github_issues_data"] = None
        
    if fetch_btn:
        if not owner or not repo:
            st.warning("Please enter both Repository Owner and Repository Name.")
        else:
            with st.spinner(f"Fetching issues for {owner}/{repo}..."):
                try:
                    issues = fetch_open_issues(owner, repo)
                    if issues:
                        st.session_state["github_issues_data"] = issues
                        st.success(f"Successfully fetched {len(issues)} open issues.")
                    else:
                        st.session_state["github_issues_data"] = []
                        st.info(f"No open issues found for {owner}/{repo}.")
                except Exception as e:
                    st.error(str(e))
                    
    # Display the issues if data is available in session state
    if st.session_state["github_issues_data"]:
        issues_list = st.session_state["github_issues_data"]
        
        # Convert to DataFrame for display
        df = pd.DataFrame(issues_list)
        
        # We might not want to show the full body in the table to save space
        display_df = df[["Issue Number", "Title", "State", "Created Date", "Updated Date"]].copy()
        
        st.markdown("### Open Issues")
        st.caption("Select a row to view issue details. Use the table search icon to filter.")
        
        # Display the dataframe with selection enabled
        selection = st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row"
        )
        
        # If a row is selected, display detailed information below the table
        selected_rows = selection.selection.rows
        if selected_rows:
            selected_index = selected_rows[0]
            selected_issue = df.iloc[selected_index]
            
            st.markdown("---")
            st.markdown(f"### Issue #{selected_issue['Issue Number']}: {selected_issue['Title']}")
            
            # Status and Dates
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown(f"**Status:** {selected_issue['State']}")
            with col_b:
                st.markdown(f"**Created Date:** {selected_issue['Created Date']}")
            with col_c:
                st.markdown(f"**Updated Date:** {selected_issue['Updated Date']}")
                
            # URL Link
            st.markdown(f"**GitHub URL:** [{selected_issue['URL']}]({selected_issue['URL']})")
            
            # Description (Body)
            st.markdown("**Description:**")
            st.info(selected_issue['Body'])
