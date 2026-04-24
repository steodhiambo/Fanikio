import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path to allow importing from 'database'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import execute_query

st.set_page_config(page_title="Content | Fanikio", layout="wide")

st.title("✍️ Content Factory")

posts = execute_query(
    "SELECT pillar, topic, status, created_at FROM posts ORDER BY created_at DESC",
    fetch=True,
)

if posts:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Post Queue")
        df_posts = pd.DataFrame(posts)
        st.dataframe(df_posts, use_container_width=True)
        
        selected_topic = st.selectbox("Select a topic to preview", [p["topic"] for p in posts])
        
    with col2:
        if selected_topic:
            st.subheader(f"Preview: {selected_topic}")
            post_data = execute_query(
                "SELECT linkedin_post, x_post, pillar FROM posts WHERE topic = %s LIMIT 1",
                (selected_topic,),
                fetch=True,
            )
            if post_data:
                p = post_data[0]
                st.info(f"Pillar: {p['pillar'].replace('_', ' ').title()}")
                
                tabs = st.tabs(["LinkedIn Version", "X Version"])
                with tabs[0]:
                    st.markdown("### LinkedIn")
                    st.code(p['linkedin_post'], language=None)
                with tabs[1]:
                    st.markdown("### X (Twitter)")
                    st.code(p['x_post'], language=None)
                    
                if st.button("Mark as Published"):
                    st.success("Post marked as published!")

else:
    st.info("No content drafts found. Run the content agent to generate posts.")
