import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
from frontend.ui_utils import render_card, status_badge

def render_dashboard():
    """
    Renders the upgraded Enterprise Dashboard page.
    """
    st.title("AI Software Auditor")
    st.subheader("Enterprise AI Developer Platform")
    
    st.markdown("---")
    
    # 1. Top Metrics Row
    st.markdown("### System Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Audits", value="1,024", delta="12 today")
    with col2:
        st.metric(label="Passed", value="850", delta="8 today")
    with col3:
        st.metric(label="Failed", value="174", delta="-2 from yesterday", delta_color="inverse")
    with col4:
        st.metric(label="Trust Score", value="91%", delta="1.2%")

    st.write("") # Spacer

    # 2. Secondary Metrics Row
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric(label="Avg AI Response Time", value="3.4s", delta="-0.2s")
    with col6:
        st.metric(label="Avg Verification Time", value="18.5s", delta="-1.5s")
    with col7:
        st.metric(label="Repositories Audited", value="42", delta="2 new")
    with col8:
        st.metric(label="Today's Audits", value="12", delta="On track")

    st.markdown("---")
    
    # 3. Charts Row
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("### Verification Success Rate")
        pie_data = pd.DataFrame({
            'Verdict': ['Passed', 'Failed'],
            'Count': [850, 174]
        })
        pie_chart = alt.Chart(pie_data).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(
                field="Verdict", 
                type="nominal", 
                scale=alt.Scale(domain=['Passed', 'Failed'], range=['#28a745', '#dc3545'])
            ),
            tooltip=['Verdict', 'Count']
        ).properties(height=350).configure_legend(orient='bottom')
        st.altair_chart(pie_chart, use_container_width=True)
        
    with chart_col2:
        st.markdown("### Trust Score Trend (30 Days)")
        dates = pd.date_range(end=datetime.today(), periods=30).strftime('%b %d')
        trend_data = pd.DataFrame({
            "Score": [80 + (i % 5) + (i*0.3) for i in range(30)]
        }, index=dates)
        st.line_chart(trend_data, height=350)

    st.markdown("---")
    
    # 4. Recent Audits Table
    st.markdown("### Recent Audits")
    recent_audits_data = {
        "Repository": ["streamlit/streamlit", "facebook/react", "vercel/next.js", "python/cpython", "microsoft/vscode"],
        "Issue ID": ["#123", "#456", "#789", "#101", "#202"],
        "Worker Claim": [
            "Fixed state management bug",
            "Optimized rendering loop",
            "Added image loader",
            "Fixed memory leak in ast.c",
            "Updated sidebar UI"
        ],
        "Verdict": ["PASS", "PASS", "FAIL", "PASS", "PASS"],
        "Time": [
            "10 mins ago", "1 hour ago", "3 hours ago", "1 day ago", "2 days ago"
        ]
    }
    
    df_recent = pd.DataFrame(recent_audits_data)
    st.dataframe(df_recent, use_container_width=True, hide_index=True)
