import streamlit as st
import time

def show_loading_step(step_name: str, duration: float = 0.5):
    """Shows a professional loading spinner and a progress bar for a step."""
    with st.spinner(f"{step_name}..."):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(duration / 100)
            progress_bar.progress(i + 1)
        progress_bar.empty()

def status_badge(status: str) -> str:
    """Returns a styled HTML badge based on status."""
    if status.upper() == "PASS":
        return "<span style='background-color: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;'>PASS</span>"
    elif status.upper() == "FAIL":
        return "<span style='background-color: #dc3545; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;'>FAIL</span>"
    return f"<span style='background-color: #6c757d; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;'>{status}</span>"
    
def render_card(title: str, content: str, icon: str = "📝"):
    """Renders a visually appealing card in Streamlit using markdown."""
    st.markdown(
        f"""
        <div style="
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #333;
            margin-bottom: 20px;
        ">
            <h4 style="margin-top:0px; color:#4dabf7;">{icon} {title}</h4>
            <div style="color: #cfcfcf;">{content}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
