"""
Weekly Strategy Dashboard
Run with: streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
from database.db import execute_query

st.set_page_config(page_title="Fanikio Dashboard", layout="wide")
st.title("Fanikio — Personal Brand Growth Dashboard")

# --- Top People to Connect With ---
st.header("Top People to Connect With This Week")
people = execute_query(
    """
    SELECT name, platform, role, company, followers, opportunity_score, why_they_matter, status
    FROM people
    WHERE status = 'discovered'
    ORDER BY opportunity_score DESC
    LIMIT 20
    """,
    fetch=True,
)
if people:
    df = pd.DataFrame(people)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No people discovered yet. Run the discovery agent first.")

st.divider()

# --- Content Queue ---
st.header("Content Queue")
posts = execute_query(
    "SELECT pillar, topic, status, created_at FROM posts ORDER BY created_at DESC LIMIT 20",
    fetch=True,
)
if posts:
    df_posts = pd.DataFrame(posts)
    st.dataframe(df_posts, use_container_width=True)

    selected_topic = st.selectbox("Preview a post", [p["topic"] for p in posts])
    if selected_topic:
        post = execute_query(
            "SELECT linkedin_post, x_post FROM posts WHERE topic = %s LIMIT 1",
            (selected_topic,),
            fetch=True,
        )
        if post:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("LinkedIn")
                st.text_area("", post[0]["linkedin_post"], height=250, key="li")
            with col2:
                st.subheader("X")
                st.text_area("", post[0]["x_post"], height=250, key="x")
else:
    st.info("No posts generated yet. Run the content agent first.")

st.divider()

# --- Engagement Suggestions ---
st.header("Today's Engagement Suggestions")
suggestions = execute_query(
    """
    SELECT author_name, original_post_text, suggested_comment, status, created_at
    FROM engagement_suggestions
    WHERE status = 'pending'
    ORDER BY created_at DESC
    LIMIT 10
    """,
    fetch=True,
)
if suggestions:
    for s in suggestions:
        with st.expander(f"@{s['author_name']} — {s['original_post_text'][:80]}..."):
            st.markdown(f"**Original post:** {s['original_post_text']}")
            st.markdown(f"**Suggested comment:** {s['suggested_comment']}")
else:
    st.info("No engagement suggestions yet. Run the engagement agent first.")

st.divider()

# --- Weekly Metrics ---
st.header("Weekly Metrics")
col1, col2, col3, col4, col5 = st.columns(5)
metrics = execute_query(
    "SELECT * FROM weekly_metrics ORDER BY week_start DESC LIMIT 1",
    fetch=True,
)
if metrics:
    m = metrics[0]
    col1.metric("New Connections", m["new_connections"], delta_color="normal")
    col2.metric("Comments Made", m["comments_made"])
    col3.metric("Posts Published", m["posts_published"])
    col4.metric("Recruiter Replies", m["recruiter_replies"])
    col5.metric("Profile Visits", m["profile_visits"])
else:
    col1.metric("New Connections", "—")
    col2.metric("Comments Made", "—")
    col3.metric("Posts Published", "—")
    col4.metric("Recruiter Replies", "—")
    col5.metric("Profile Visits", "—")
    st.info("No weekly metrics yet. Update them manually or via the metrics logger.")
