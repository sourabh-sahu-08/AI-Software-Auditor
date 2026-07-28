import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

def render_analytics():
    st.title("Analytics")
    st.markdown("System-wide metrics and performance indicators.")
    
    # Generate mock historical data
    dates = [datetime.today() - timedelta(days=x) for x in range(30, 0, -1)]
    
    # 1. Trust Score Trend
    trust_scores = [85 + (i * 0.2) + random.uniform(-1, 2) for i in range(30)]
    df_trust = pd.DataFrame({'Date': dates, 'Trust Score': trust_scores})
    
    fig_trust = px.line(df_trust, x='Date', y='Trust Score', title='Trust Score Trend (30 Days)')
    fig_trust.update_layout(template="plotly_dark")
    st.plotly_chart(fig_trust, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 2. Verification Success Rate
        success_data = pd.DataFrame({
            'Result': ['Passed', 'Failed'],
            'Count': [850, 150]
        })
        fig_success = px.pie(success_data, values='Count', names='Result', title='Verification Success Rate', hole=0.4, color='Result', color_discrete_map={'Passed':'#28a745', 'Failed':'#dc3545'})
        fig_success.update_layout(template="plotly_dark")
        st.plotly_chart(fig_success, use_container_width=True)
        
    with col2:
        # 3. Average Execution Time
        exec_times = [15, 16, 14, 18, 17, 19, 15, 14, 13, 16, 17, 15, 16, 18, 19, 18, 17, 16, 15, 14, 15, 16, 17, 18, 19, 17, 16, 15, 14, 15]
        df_exec = pd.DataFrame({'Date': dates, 'Execution Time (s)': exec_times})
        fig_exec = px.bar(df_exec, x='Date', y='Execution Time (s)', title='Average Verification Time')
        fig_exec.update_layout(template="plotly_dark")
        st.plotly_chart(fig_exec, use_container_width=True)
        
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    
    with col3:
        # 4. Most Common Failures
        failure_data = pd.DataFrame({
            'Failure Type': ['Lint Errors', 'Unit Test Fails', 'Security Vulns', 'Build Fails'],
            'Count': [85, 45, 12, 8]
        })
        fig_fails = px.bar(failure_data, x='Count', y='Failure Type', orientation='h', title='Most Common Failures')
        fig_fails.update_layout(template="plotly_dark")
        st.plotly_chart(fig_fails, use_container_width=True)
        
    with col4:
        # 5. Top Audited Repositories
        repo_data = pd.DataFrame({
            'Repository': ['streamlit/streamlit', 'facebook/react', 'vercel/next.js', 'microsoft/vscode', 'python/cpython'],
            'Audits': [120, 85, 60, 45, 30]
        })
        fig_repos = px.bar(repo_data, x='Repository', y='Audits', title='Top Audited Repositories')
        fig_repos.update_layout(template="plotly_dark")
        st.plotly_chart(fig_repos, use_container_width=True)
