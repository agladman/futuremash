#!/usr/bin/env Python3

"""corpusbuilder.py: a script to scrape submission headlines from tech
    news subreddits and create a corpus from which Markov chains can be
    generated.
    """


import praw
import yaml


with open('config/config.yml', 'r') as f:
    try:
        cfg = yaml.load(f)
    except yaml.YAMLError as exc:
        print(exc)

if cfg:
    my_user_agent = cfg['reddit']['my_user_agent']
    my_client_id = cfg['reddit']['my_client_id']
    my_client_secret = cfg['reddit']['my_client_secret']
    my_username = cfg['reddit']['my_username']
    my_password = cfg['reddit']['my_password']

reddit = praw.Reddit(user_agent=my_user_agent,
                     client_id=my_client_id,
                     client_secret=my_client_secret,
                     username=my_username,
                     password=my_password)

subs = ['tech', 'technews', 'gadgets', 'tech_news_today']

for sub in subs:
    subreddit = reddit.subreddit(sub)
    for submission in subreddit.hot(limit=10):
        print(submission.title)  # Output: the title of the submission
        print(submission.ups)    # Output: upvote count
        print(submission.id)     # Output: the ID of the submission
