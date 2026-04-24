import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path to allow importing from 'database'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import execute_query

st.set_page_config(page_title="Networking | Fanikio", layout="wide")

st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤝 Networking Strategy")
st.subheader("Top Opportunity People")

people = execute_query(
    """
    SELECT name, platform, role, company, followers, opportunity_score, why_they_matter, status
    FROM people
    WHERE status = 'discovered'
    ORDER BY opportunity_score DESC
    LIMIT 50
    """,
    fetch=True,
)

if people:
    df = pd.DataFrame(people)
    # Highlight high opportunity scores
    st.dataframe(
        df.style.background_gradient(subset=['opportunity_score'], cmap='viridis'),
        use_container_width=True
    )
    
    st.divider()
    
    # Manual entry for LinkedIn
    with st.expander("➕ Add Person Manually (LinkedIn)"):
        with st.form("manual_add"):
            name = st.text_input("Name")
            role = st.text_input("Role")
            company = st.text_input("Company")
            profile_url = st.text_input("Profile URL")
            followers = st.number_input("Followers", min_value=0, step=100)
            submitted = st.form_submit_button("Add Connection")
            if submitted:
                # Add logic or call agent script
                st.success(f"Added {name} to discovery queue.")

else:
    st.info("No people discovered yet. Run the discovery agent to find peers and recruiters.")
