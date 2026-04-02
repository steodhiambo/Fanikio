"""
Agent 1: People Discovery Agent
- Searches X (Twitter) using hashtags via Tweepy
- Accepts manual LinkedIn entries
- Saves discovered people to the database
"""

import tweepy
from datetime import datetime
from config import (
    X_BEARER_TOKEN,
    X_HASHTAGS,
)
from database.db import execute_query


def save_person(name, platform, role, company, profile_url, followers):
    query = """
        INSERT INTO people (name, platform, role, company, profile_url, followers)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """
    execute_query(query, (name, platform, role, company, profile_url, followers))
    print(f"Saved: {name} [{platform}]")


# --- X Discovery ---

def search_x_users(hashtag, max_results=20):
    client = tweepy.Client(bearer_token=X_BEARER_TOKEN)
    query = f"{hashtag} -is:retweet lang:en"

    try:
        response = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            expansions=["author_id"],
            user_fields=["name", "username", "description", "public_metrics"],
        )
    except tweepy.TweepyException as e:
        print(f"X API error for {hashtag}: {e}")
        return

    if not response.includes or "users" not in response.includes:
        print(f"No users found for {hashtag}")
        return

    for user in response.includes["users"]:
        name = user.name
        username = user.username
        description = user.description or ""
        followers = user.public_metrics.get("followers_count", 0)
        profile_url = f"https://x.com/{username}"

        # Infer role from bio
        role = infer_role_from_bio(description)

        save_person(
            name=name,
            platform="x",
            role=role,
            company=None,
            profile_url=profile_url,
            followers=followers,
        )


def infer_role_from_bio(bio: str) -> str:
    bio_lower = bio.lower()
    if any(word in bio_lower for word in ["recruiter", "talent", "hiring"]):
        return "Recruiter"
    if any(word in bio_lower for word in ["cto", "chief technology"]):
        return "CTO"
    if any(word in bio_lower for word in ["founder", "co-founder"]):
        return "Founder"
    if "head of data" in bio_lower:
        return "Head of Data"
    if any(word in bio_lower for word in ["data engineer", "analytics engineer"]):
        return "Data Engineer"
    if "data analyst" in bio_lower:
        return "Data Analyst"
    if "engineering manager" in bio_lower:
        return "Engineering Manager"
    return "Data Professional"


def run_x_discovery():
    print("Starting X discovery...")
    for hashtag in X_HASHTAGS:
        print(f"Searching {hashtag}...")
        search_x_users(hashtag)
    print("X discovery complete.")


# --- LinkedIn Manual Input ---

def add_linkedin_person_manually():
    print("\n--- Add LinkedIn Person ---")
    name = input("Name: ").strip()
    role = input("Role/Title: ").strip()
    company = input("Company: ").strip()
    profile_url = input("Profile URL: ").strip()
    followers = input("Followers/Connections (press Enter to skip): ").strip()
    followers = int(followers) if followers.isdigit() else 0

    save_person(
        name=name,
        platform="linkedin",
        role=role,
        company=company,
        profile_url=profile_url,
        followers=followers,
    )


def bulk_add_linkedin(people: list[dict]):
    """
    Programmatically add multiple LinkedIn people.
    Each dict: {name, role, company, profile_url, followers}
    """
    for p in people:
        save_person(
            name=p.get("name"),
            platform="linkedin",
            role=p.get("role"),
            company=p.get("company"),
            profile_url=p.get("profile_url"),
            followers=p.get("followers", 0),
        )


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "linkedin":
        add_linkedin_person_manually()
    else:
        run_x_discovery()
