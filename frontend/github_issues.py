import streamlit as st
import pandas as pd
from backend.github_service import fetch_open_issues
from backend.error_handlers import handle_error
from frontend.ui_utils import show_loading_step, render_card

def render_github_issues():
    st.title("GitHub Issues")
    st.markdown("Fetch and manage open issues for verification and AI Analysis.")
    
    col1, col2 = st.columns(2)
    with col1:
        owner = st.text_input("Repository Owner", placeholder="e.g., streamlit")
    with col2:
        repo = st.text_input("Repository Name", placeholder="e.g., streamlit")
        
    fetch_btn = st.button("Fetch Issues", type="primary")
    
    if "github_issues_data" not in st.session_state:
        st.session_state["github_issues_data"] = None
        
    if fetch_btn:
        if not owner or not repo:
            st.warning("Please enter both Repository Owner and Repository Name.")
        else:
            try:
                show_loading_step(f"Fetching issues for {owner}/{repo}", 1.5)
                issues = fetch_open_issues(owner, repo)
                if issues:
                    st.session_state["github_issues_data"] = issues
                    st.success(f"Successfully fetched {len(issues)} open issues.")
                else:
                    st.session_state["github_issues_data"] = []
                    st.info(f"No open issues found for {owner}/{repo}.")
            except Exception as e:
                handle_error("GitHub API Fetch", e)
                    
    if st.session_state["github_issues_data"]:
        issues_list = st.session_state["github_issues_data"]
        df = pd.DataFrame(issues_list)
        
        display_df = df[["Issue Number", "Title", "Author", "Comments", "State"]].copy()
        
        st.markdown("### Open Issues")
        st.caption("Select a row to view issue details. Use the table search icon to filter.")
        
        selection = st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row"
        )
        
        selected_rows = selection.selection.rows
        if selected_rows:
            selected_index = selected_rows[0]
            selected_issue = df.iloc[selected_index]
            
            st.markdown("---")
            
            # Use st.expander for a clean layout
            with st.expander(f"View Details: #{selected_issue['Issue Number']} {selected_issue['Title']}", expanded=True):
                col_a, col_b, col_c, col_d = st.columns(4)
                with col_a: st.markdown(f"**Author:** {selected_issue['Author']}")
                with col_b: st.markdown(f"**Labels:** {selected_issue['Labels']}")
                with col_c: st.markdown(f"**Created:** {selected_issue['Created Date'][:10]}")
                with col_d: st.markdown(f"**Comments:** {selected_issue['Comments']}")
                    
                st.markdown(f"**GitHub URL:** [{selected_issue['URL']}]({selected_issue['URL']})")
                
                st.markdown("**Description:**")
                st.info(selected_issue['Body'])
            
            st.markdown("### AI Analysis")
            issue_number = selected_issue['Issue Number']
            
            if "ai_analysis" not in st.session_state:
                st.session_state["ai_analysis"] = {}
                
            if st.button("Analyze with AI", type="primary", key=f"analyze_{issue_number}"):
                try:
                    import time
                    from backend.worker_agent import analyze_issue
                    show_loading_step("AI Worker is analyzing the issue...", 2.5)
                    start_time = time.time()
                    analysis = analyze_issue(selected_issue['Title'], selected_issue['Body'])
                    end_time = time.time()
                    
                    st.session_state["ai_analysis"][issue_number] = {
                        "data": analysis,
                        "time": round(end_time - start_time, 2),
                        "title": selected_issue['Title']
                    }
                    st.success("Analysis Complete! Navigate to the 'Worker Analysis' tab to view results.")
                except Exception as e:
                    handle_error("AI Analysis", e)
