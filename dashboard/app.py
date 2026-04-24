import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path to allow importing from 'database'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import execute_query

st.set_page_config(page_title="Fanikio | AI Personal Branding", layout="wide")

# Custom Premium Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    
    .stMetric {
        background: rgba(30, 41, 59, 0.7);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .css-1r6p78m { # Sidebar
        background-color: #0f172a;
    }
    
    h1, h2, h3 {
        color: #6366f1;
        font-weight: 700;
    }
    
    .card {
        background: rgba(30, 41, 59, 0.7);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Fanikio Command Center")
st.markdown("### Accelerate your personal brand with AI-driven networking and content.")

# --- Summary Metrics ---
st.header("Weekly Overview")
col1, col2, col3, col4, col5 = st.columns(5)

# Mock some metrics if none exist
metrics = execute_query(
    "SELECT * FROM weekly_metrics ORDER BY week_start DESC LIMIT 1",
    fetch=True,
)

if metrics:
    m = metrics[0]
else:
    m = {
        "new_connections": 12,
        "comments_made": 24,
        "posts_published": 3,
        "recruiter_replies": 2,
        "profile_visits": 145
    }

col1.metric("New Connections", m["new_connections"], "+3")
col2.metric("Comments Made", m["comments_made"], "+8")
col3.metric("Posts Published", m["posts_published"], "+1")
col4.metric("Recruiter Replies", m["recruiter_replies"], "+1")
col5.metric("Profile Visits", m["profile_visits"], "+15%")

st.divider()

# --- Quick Links / Summary ---
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("""
    <div class="card">
        <h3>🎯 Current Goal</h3>
        <p>Your goal this week is to connect with <b>20 quality data professionals</b> and maintain a <b>daily posting schedule</b>.</p>
        <p><b>Top Hashtags:</b> #dataengineering, #analytics, #dbt</p>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div class="card">
        <h3>🛠️ Next Actions</h3>
        <ul>
            <li>Review 5 new networking opportunities</li>
            <li>Schedule 2 content drafts for tomorrow</li>
            <li>Reply to 10 community posts</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.success("Select a strategy area above to get started.")
st.sidebar.markdown("---")
st.sidebar.markdown("### Current Environment")
st.sidebar.info("Running in **MOCK MODE** (Local SQLite)")
