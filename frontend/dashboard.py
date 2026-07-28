import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

def render_dashboard():
    """
    Renders the Dashboard page including metric cards, charts, and a recent audits table.
    Uses sample/placeholder data as requested.
    """
    # Header and Subtitle
    st.title("AI Software Auditor")
    st.subheader("Monitor AI software engineers and verify their claims.")
    
    st.markdown("---")
    
    # 1. Metric Cards
    # Using Streamlit columns for responsive layout
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Audits", value="24")
    with col2:
        st.metric(label="Passed", value="18")
    with col3:
        st.metric(label="Failed", value="6")
    with col4:
        st.metric(label="Trust Score", value="91%")
        
    st.markdown("---")
    
    # 2. Charts Row
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("### Audit Verdicts")
        # Pie chart using Altair to show Passed vs Failed
        pie_data = pd.DataFrame({
            'Verdict': ['Passed', 'Failed'],
            'Count': [18, 6]
        })
        
        # Create a donut chart (pie chart with inner radius) using Altair
        pie_chart = alt.Chart(pie_data).mark_arc(innerRadius=40).encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(
                field="Verdict", 
                type="nominal", 
                scale=alt.Scale(domain=['Passed', 'Failed'], range=['#2e7b32', '#d32f2f'])
            ),
            tooltip=['Verdict', 'Count']
        ).properties(
            height=300
        ).configure_legend(
            orient='bottom'
        )
        st.altair_chart(pie_chart, use_container_width=True)
        
    with chart_col2:
        st.markdown("### Trust Score Trend")
        # Line chart showing trust score trend over time
        # Generate sample date indices for the last 7 days
        dates = pd.date_range(end=datetime.today(), periods=7).strftime('%b %d')
        trend_data = pd.DataFrame({
            "Trust Score": [85, 87, 86, 88, 90, 89, 91]
        }, index=dates)
        
        # Use native Streamlit line chart
        st.line_chart(trend_data, height=300)

    st.markdown("---")
    
    # 3. Recent Audits Table
    st.markdown("### Recent Audits")
    
    # Sample data for the Recent Audits table
    recent_audits_data = {
        "Issue ID": ["#101", "#102", "#103", "#104", "#105"],
        "Issue Title": [
            "Fix login page bug",
            "Optimize database queries",
            "Update API documentation",
            "Refactor authentication flow",
            "Implement dark mode"
        ],
        "Worker Claim": [
            "Fixed null pointer exception",
            "Added indexes to users table",
            "Updated Swagger UI",
            "Migrated to OAuth 2.0",
            "Added CSS variables for dark theme"
        ],
        "Verdict": ["Passed", "Passed", "Failed", "Passed", "Passed"],
        "Timestamp": [
            (datetime.now() - timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M"),
            (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
            (datetime.now() - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"),
            (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
            (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M"),
        ]
    }
    
    df_recent = pd.DataFrame(recent_audits_data)
    
    # Render the dataframe cleanly without the index
    st.dataframe(
        df_recent,
        use_container_width=True,
        hide_index=True
    )
