"""
Agent 2: Opportunity Scoring Agent
- Scores all unscored people using the weighted formula
- Uses GPT to generate "why they matter" summaries
- Updates scores in the database
"""

from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, SCORING_WEIGHTS
from database.db import execute_query

client = OpenAI(api_key=OPENAI_API_KEY)


def score_person(person: dict) -> dict:
    role = (person.get("role") or "").lower()
    followers = person.get("followers") or 0

    # Hiring potential (0-10): based on role keywords
    hiring_keywords = ["recruiter", "talent", "hiring", "head of data", "cto", "founder", "engineering manager"]
    hiring = 9 if any(k in role for k in hiring_keywords) else 4

    # Relevance (0-10): based on data engineering role keywords
    relevance_keywords = ["data engineer", "analytics engineer", "data analyst", "dbt", "databricks", "airflow", "spark"]
    relevance = 9 if any(k in role for k in relevance_keywords) else 6

    # Activity (0-10): placeholder — can be enriched with post frequency later
    activity = 7

    # Influence (0-10): based on follower count
    if followers >= 10000:
        influence = 9
    elif followers >= 1000:
        influence = 7
    elif followers >= 100:
        influence = 5
    else:
        influence = 3

    w = SCORING_WEIGHTS
    opportunity_score = round(
        hiring * w["hiring_potential"]
        + relevance * w["relevance"]
        + activity * w["activity"]
        + influence * w["influence"],
        2,
    )

    return {
        "hiring_potential": hiring,
        "relevance_score": relevance,
        "activity_score": activity,
        "influence_score": influence,
        "opportunity_score": opportunity_score,
    }


def generate_why_they_matter(person: dict) -> str:
    prompt = f"""
You are a career strategist. In 1-2 sentences, explain why this person is worth connecting with
for someone who is an aspiring data engineer and analytics engineer learning dbt, Databricks, Airflow, Spark, SQL, and Python.

Person:
- Name: {person.get('name')}
- Platform: {person.get('platform')}
- Role: {person.get('role')}
- Company: {person.get('company') or 'Unknown'}
- Followers: {person.get('followers')}

Be specific and practical. Do not be generic.
"""
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
    )
    return response.choices[0].message.content.strip()


def run_scoring():
    people = execute_query(
        "SELECT * FROM people WHERE opportunity_score = 0 OR opportunity_score IS NULL",
        fetch=True,
    )

    if not people:
        print("No unscored people found.")
        return

    print(f"Scoring {len(people)} people...")

    for person in people:
        scores = score_person(person)
        why = generate_why_they_matter(person)

        execute_query(
            """
            UPDATE people SET
                hiring_potential = %s,
                relevance_score = %s,
                activity_score = %s,
                influence_score = %s,
                opportunity_score = %s,
                why_they_matter = %s,
                updated_at = NOW()
            WHERE id = %s
            """,
            (
                scores["hiring_potential"],
                scores["relevance_score"],
                scores["activity_score"],
                scores["influence_score"],
                scores["opportunity_score"],
                why,
                person["id"],
            ),
        )
        print(f"Scored {person['name']}: {scores['opportunity_score']} — {why}")

    print("Scoring complete.")


if __name__ == "__main__":
    run_scoring()
