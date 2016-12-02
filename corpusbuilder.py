#!/usr/bin/env Python3

"""corpusbuilder.py: a script to scrape submission headlines from tech
    news subreddits and create a corpus from which Markov chains can be
    generated.
    """


import os
import praw
import time
import uuid
import yaml


# read from config file and set variables
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
    corpus_age_limit = cfg['age']['corpus_age_limit_days']
    subs = cfg['subreddits']

reddit = praw.Reddit(user_agent=my_user_agent,
                     client_id=my_client_id,
                     client_secret=my_client_secret,
                     username=my_username,
                     password=my_password)


def clean_corpus():
    path = 'corpus/'
    paths = [os.path.join(path, fname) for fname in os.listdir(path)]
    for file in paths:
        m = os.path.getctime(file)  # could try os.path.getmtime()
        now = time.time()
        limit = now - corpus_age_limit_to_seconds()
        if m < limit:
            os.remove(file)


def corpus_age_limit_to_seconds():
    x = 60 * 60 * 24 * corpus_age_limit
    return x


def pull_from_reddit():
    with open('config/checked.txt', 'r') as f:
        checked = f.read().splitlines()
        output = []
        for sub in subs:
            subreddit = reddit.subreddit(sub)
            for submission in subreddit.hot(limit=10):
                if submission.id not in checked:
                    # check on ups not implemented as pulling from .hot
                    # if submission.ups > somelimit
                    output.append(submission.title)
                    checked.append(submission.id)
    if len(output) == 0:
        print('No new submissions found')
    else:
        output_filename = '{0}.txt'.format(uuid.uuid4().hex)
        with open('corpus/{0}'.format(output_filename), 'a') as f:
            for item in output:
                f.write(item + '\n')
    with open('config/checked.txt', 'a') as f:
        for item in checked:
            f.write(item + '\n')


if __name__ == '__main__':
    clean_corpus()
    pull_from_reddit()
