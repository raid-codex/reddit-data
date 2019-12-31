import praw
import json
import datetime
import os

reddit = praw.Reddit(client_id=os.getenv("REDDIT_CLIENT_ID"),
                     client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                     user_agent='python:com.raid-codex.reddit:v1.0 (by /u/raidcodex)')
subreddit = reddit.subreddit("RaidShadowLegends")

this_month = datetime.datetime.now().strftime("%Y-%m")


def store(submissions, filename):
    data = []
    for submission in submissions:
        if submission.stickied:
            continue
        post = {
            'title': submission.title,
            'permalink': submission.permalink,
            'url': submission.url,
            'author': submission.author.name,
            'score': submission.score,
            'id': submission.id,
            'created_at': datetime.datetime.fromtimestamp(submission.created_utc).isoformat()+"+00:00",
        }
        if hasattr(submission, "preview"):
            post['preview'] = submission.preview
        data.append(post)
    with open(filename, "w") as file:
        json.dump(data, file, sort_keys=True, indent=4, separators=(',', ': '))


store(submissions=subreddit.top("month", limit=30),
      filename="./docs/submissions/top/{}.json".format(this_month))
