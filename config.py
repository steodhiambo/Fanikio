import os
from dotenv import load_dotenv

load_dotenv()

# Database
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", 5432),
    "dbname": os.getenv("DB_NAME", "fanikio"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"

# X (Twitter) API
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.getenv("X_ACCESS_SECRET")
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")

# Discovery targets
X_HASHTAGS = [
    "#dataengineering",
    "#analyticsengineering",
    "#dbt",
    "#databricks",
    "#airflow",
    "#sql",
    "#python",
    "#hiring",
]

LINKEDIN_SEARCH_TERMS = [
    "Data Engineer Recruiter",
    "Hiring Data Analyst",
    "Head of Data",
    "Founder AND data platform",
    "dbt engineer",
    "Databricks hiring",
]

# Scoring weights
SCORING_WEIGHTS = {
    "hiring_potential": 0.40,
    "relevance": 0.25,
    "activity": 0.20,
    "influence": 0.15,
}

# Content pillars
CONTENT_PILLARS = [
    "what_i_learned",
    "mini_tutorial",
    "project_breakdown",
    "opinion",
    "career_journey",
]
