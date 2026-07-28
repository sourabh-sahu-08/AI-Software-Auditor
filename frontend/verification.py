import streamlit as st
import os
from backend.build_runner import run_build
from backend.test_runner import run_tests
from backend.lint_runner import run_lint
from backend.security_runner import run_security
from frontend.ui_utils import show_loading_step, status_badge
from backend.logger import log_verification

def render_verification():
    st.title("Verification Engine")
    st.markdown("Run objective checks on the codebase.")
    
    # Pre-select one of our sample projects
    base_dir = os.path.dirname(os.path.dirname(__file__))
    sample_dir = os.path.join(base_dir, "sample_projects")
    projects = []
    if os.path.exists(sample_dir):
        projects = [d for d in os.listdir(sample_dir) if os.path.isdir(os.path.join(sample_dir, d))]
        
    if not projects:
        st.warning("No sample projects found.")
        return
        
    selected_project = st.selectbox("Select a project to verify:", projects)
    project_path = os.path.join(sample_dir, selected_project)
    
    if st.button("Run Verification Suite", type="primary"):
        # We store results in session state to display them across re-runs
        st.session_state["verification_results"] = {}
        
        st.write("---")
        
        # Build
        show_loading_step("Running Build...")
        build_res = run_build(project_path)
        log_verification("Build", build_res["status"], build_res["execution_time"])
        st.session_state["verification_results"]["Build"] = build_res
        
        # Tests
        show_loading_step("Running Tests...")
        test_res = run_tests(project_path)
        log_verification("Tests", test_res["status"], test_res["execution_time"])
        st.session_state["verification_results"]["Tests"] = test_res
        
        # Lint
        show_loading_step("Running Lint...")
        lint_res = run_lint(project_path)
        log_verification("Lint", lint_res["status"], lint_res["execution_time"])
        st.session_state["verification_results"]["Lint"] = lint_res
        
        # Security
        show_loading_step("Running Security Scan...")
        sec_res = run_security(project_path)
        log_verification("Security", sec_res["status"], sec_res["execution_time"])
        st.session_state["verification_results"]["Security"] = sec_res
        
        st.success("Verification Completed!")
        
    # Render results if available
    if "verification_results" in st.session_state and st.session_state["verification_results"]:
        results = st.session_state["verification_results"]
        
        for step_name in ["Build", "Tests", "Lint", "Security"]:
            res = results.get(step_name)
            if not res: continue
            
            with st.container(border=True):
                col1, col2 = st.columns([1, 5])
                with col1:
                    st.markdown(status_badge(res['status']), unsafe_allow_html=True)
                with col2:
                    st.markdown(f"**{step_name}** ({res['execution_time']}s)")
                    
                # Specific metrics based on step
                if step_name == "Tests":
                    st.caption(f"Passed: {res.get('tests_passed', 0)} | Failed: {res.get('tests_failed', 0)}")
                elif step_name == "Lint":
                    st.caption(f"Warnings: {res.get('warnings', 0)} | Errors: {res.get('errors', 0)}")
                elif step_name == "Security":
                    st.caption(f"High: {res.get('high', 0)} | Medium: {res.get('medium', 0)} | Low: {res.get('low', 0)}")
                    
                with st.expander("View Logs"):
                    st.code(res.get("output", "No output provided."), language="text")
