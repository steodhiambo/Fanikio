"""
Agent 3: Content Creation Agent
- Generates LinkedIn posts + X threads using GPT
- Covers all 5 content pillars
- Saves drafts to the database
"""

from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL
from database.db import execute_query

client = OpenAI(api_key=OPENAI_API_KEY)

PILLAR_PROMPTS = {
    "what_i_learned": "Share a genuine lesson learned while working with {topic}. Start with what you got wrong, then what you discovered.",
    "mini_tutorial": "Write a simple, practical explanation of {topic} that clears up a common confusion. Use a numbered list.",
    "project_breakdown": "Break down a project involving {topic}: problem, tools used, architecture, what was hard, what you learned.",
    "opinion": "Share a strong, specific opinion about {topic} in the data engineering world. Back it with a practical reason.",
    "career_journey": "Write a personal growth post about your journey with {topic}. Show before vs after understanding.",
}

SYSTEM_PROMPT = """You are a personal content strategist for an aspiring data engineer and analytics engineer.

Their audience: recruiters, founders, heads of data, data engineers, analytics professionals.
Their stack: dbt, Databricks, Airflow, Spark, SQL, Python, data pipelines.

Rules:
- Sound like a real person, not AI
- Start with a strong hook (no "I" as first word)
- Be practical and specific
- No fluff or generic advice
- Include a personal lesson or insight
- End LinkedIn posts with a question to drive comments
- Add 3 relevant hashtags at the end of LinkedIn posts"""


def generate_post(pillar: str, topic: str) -> dict:
    user_prompt = f"""
{PILLAR_PROMPTS[pillar].format(topic=topic)}

Generate:
1. A LinkedIn post (150-250 words)
2. An X thread version (under 280 characters, punchy)

Format your response exactly like this:
LINKEDIN:
[post here]

X:
[post here]
"""
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=600,
    )

    raw = response.choices[0].message.content.strip()
    linkedin_post, x_post = parse_response(raw)

    return {"linkedin": linkedin_post, "x": x_post}


def parse_response(raw: str) -> tuple[str, str]:
    linkedin_post = ""
    x_post = ""
    if "LINKEDIN:" in raw and "X:" in raw:
        parts = raw.split("X:")
        linkedin_part = parts[0].replace("LINKEDIN:", "").strip()
        x_part = parts[1].strip()
        linkedin_post = linkedin_part
        x_post = x_part
    else:
        linkedin_post = raw
    return linkedin_post, x_post


def save_post(pillar: str, topic: str, linkedin: str, x: str):
    execute_query(
        "INSERT INTO posts (pillar, topic, linkedin_post, x_post) VALUES (%s, %s, %s, %s)",
        (pillar, topic, linkedin, x),
    )


def generate_batch(ideas: list[dict]):
    """
    ideas: list of {pillar, topic}
    Example: [{"pillar": "what_i_learned", "topic": "dbt staging models"}]
    """
    for idea in ideas:
        pillar = idea["pillar"]
        topic = idea["topic"]
        print(f"\nGenerating [{pillar}] — {topic}...")
        result = generate_post(pillar, topic)
        save_post(pillar, topic, result["linkedin"], result["x"])
        print(f"LinkedIn:\n{result['linkedin']}\n")
        print(f"X:\n{result['x']}\n")
        print("-" * 60)


DEFAULT_IDEAS = [
    {"pillar": "what_i_learned", "topic": "dbt staging models"},
    {"pillar": "mini_tutorial", "topic": "difference between Spark and pandas"},
    {"pillar": "project_breakdown", "topic": "Airflow + dbt + Databricks pipeline"},
    {"pillar": "opinion", "topic": "why every data analyst should learn SQL before dashboards"},
    {"pillar": "career_journey", "topic": "understanding distributed data with Spark"},
]


if __name__ == "__main__":
    generate_batch(DEFAULT_IDEAS)
