"""
Agent 4: Engagement Agent
- Fetches top 10 relevant posts from X daily
- Uses GPT to suggest thoughtful comments
- Saves suggestions to the database for manual review
"""

import tweepy
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, X_BEARER_TOKEN, X_HASHTAGS
from database.db import execute_query

client = OpenAI(api_key=OPENAI_API_KEY)


def fetch_top_posts(max_per_hashtag=3) -> list[dict]:
    x_client = tweepy.Client(bearer_token=X_BEARER_TOKEN)
    posts = []

    for hashtag in X_HASHTAGS[:4]:  # limit to top 4 hashtags daily
        query = f"{hashtag} -is:retweet lang:en min_faves:5"
        try:
            response = x_client.search_recent_tweets(
                query=query,
                max_results=max_per_hashtag,
                expansions=["author_id"],
                tweet_fields=["text", "public_metrics"],
                user_fields=["name", "username"],
            )
        except tweepy.TweepyException as e:
            print(f"X API error for {hashtag}: {e}")
            continue

        if not response.data:
            continue

        users = {u.id: u for u in response.includes.get("users", [])}

        for tweet in response.data:
            author = users.get(tweet.author_id)
            posts.append({
                "text": tweet.text,
                "url": f"https://x.com/i/web/status/{tweet.id}",
                "author": author.name if author else "Unknown",
            })

    return posts[:10]  # cap at 10


def generate_comment(post_text: str) -> str:
    prompt = f"""
You are helping an aspiring data engineer engage meaningfully on X.

Original post:
\"{post_text}\"

Write a short, thoughtful comment (2-4 sentences) that:
1. Mentions what is interesting about the post
2. Adds one useful insight from a data engineering perspective
3. Ends with a genuine question

Sound like a real person. Be specific, not generic.
"""
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
    )
    return response.choices[0].message.content.strip()


def save_suggestion(platform, url, post_text, author, comment):
    execute_query(
        """
        INSERT INTO engagement_suggestions
            (platform, original_post_url, original_post_text, author_name, suggested_comment)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (platform, url, post_text, author, comment),
    )


def run_engagement():
    print("Fetching top posts from X...")
    posts = fetch_top_posts()

    if not posts:
        print("No posts found today.")
        return

    print(f"Generating comments for {len(posts)} posts...\n")

    for post in posts:
        comment = generate_comment(post["text"])
        save_suggestion("x", post["url"], post["text"], post["author"], comment)
        print(f"Post by @{post['author']}:\n{post['text']}\n")
        print(f"Suggested comment:\n{comment}\n")
        print("-" * 60)

    print("Engagement suggestions saved.")


if __name__ == "__main__":
    run_engagement()
