"""
Streamlit Chat UI for Fitness AI Agent
"""

import streamlit as st
from components.chat_ui import render_chat_interface
from components.goal_form import render_goal_form
from components.weekly_view import render_weekly_summary
from services.api_client import APIClient

# Page config
st.set_page_config(page_title="Fitness AI Agent", page_icon="💪", layout="wide")

# Initialize API client
if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient(base_url="http://localhost:8000/api")

# Initialize user ID (in production, use auth)
if "user_id" not in st.session_state:
    st.session_state.user_id = "demo_user"

# Sidebar
with st.sidebar:
    st.title("💪 Fitness AI Agent")
    st.markdown("---")

    page = st.radio("Navigation", ["Chat", "Goals", "Weekly Summary"])

    st.markdown("---")
    st.caption(f"User: {st.session_state.user_id}")

# Main content
if page == "Chat":
    render_chat_interface()
elif page == "Goals":
    render_goal_form()
elif page == "Weekly Summary":
    render_weekly_summary()
