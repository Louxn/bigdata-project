import praw
from dotenv import load_dotenv
import os

# Charger les variables d'environnement du .env
load_dotenv()

def create_reddit_client():
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )
    return reddit

def search_subreddit(reddit, subreddit_name, query, limit=100):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for submission in subreddit.search(query, limit=limit):
        posts.append({
            "title": submission.title,
            "score": submission.score,
            "url": submission.url,
            "num_comments": submission.num_comments,
            "created_utc": submission.created_utc,
            "selftext": submission.selftext,
            "id": submission.id,
            "author": str(submission.author)
        })
    return posts
