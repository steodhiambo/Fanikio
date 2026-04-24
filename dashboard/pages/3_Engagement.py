import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path to allow importing from 'database'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import execute_query

st.set_page_config(page_title="Engagement | Fanikio", layout="wide")

st.title("💬 Engagement Engine")
st.subheader("Daily Comment Suggestions")

suggestions = execute_query(
    """
    SELECT id, author_name, original_post_text, suggested_comment, status, created_at, original_post_url
    FROM engagement_suggestions
    WHERE status = 'pending'
    ORDER BY created_at DESC
    """,
    fetch=True,
)

if suggestions:
    for s in suggestions:
        with st.container(border=True):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**Post by {s['author_name']}**")
                st.markdown(f"> {s['original_post_text']}")
                st.markdown(f"**💡 Suggestion:** {s['suggested_comment']}")
            with col_b:
                st.link_button("View Original Post", s['original_post_url'])
                if st.button("Used", key=f"used_{s['id']}"):
                    st.success("Nice work!")
                if st.button("Skip", key=f"skip_{s['id']}"):
                    st.info("Skipped")
else:
    st.info("No pending engagement suggestions. Run the engagement agent to find posts to comment on.")
