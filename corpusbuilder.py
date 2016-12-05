#!/usr/bin/env Python3

"""corpusbuilder.py: a script to scrape submission headlines from tech
    news subreddits and create a corpus from which Markov chains can be
    generated.
    """


import logging.config
import os
import praw
import re
import time
from twython import Twython
import uuid
import yaml


log_cfg = yaml.load(open('config/logging.yml', 'r'))
logging.config.dictConfig(log_cfg)
logger = logging.getLogger(__name__)

# read from config file and set variables
with open('config/config.yml', 'r') as f:
    try:
        cfg = yaml.load(f)
    except yaml.YAMLError as exc:
        logger.error(exc)

if cfg:
    my_user_agent = cfg['reddit']['my_user_agent']
    my_client_id = cfg['reddit']['my_client_id']
    my_client_secret = cfg['reddit']['my_client_secret']
    my_username = cfg['reddit']['my_username']
    my_password = cfg['reddit']['my_password']
    corpus_age_limit = cfg['age']['corpus_age_limit_days']
    checked_logs_age_limit = cfg['age']['checked_logs_age_limit_days']
    subs = cfg['subreddits']
    APP_KEY = cfg['twitter']['app_key']
    APP_SECRET = cfg['twitter']['app_key_secret']
    OAUTH_TOKEN = cfg['twitter']['access_token']
    OAUTH_TOKEN_SECRET = cfg['twitter']['access_token_secret']
    logger.debug('loaded config')

twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

twitter.verify_credentials()

reddit = praw.Reddit(user_agent=my_user_agent,
                     client_id=my_client_id,
                     client_secret=my_client_secret,
                     username=my_username,
                     password=my_password)


def main():
    logger.info('start')
    clean_corpus()
    clean_logs()
    pull_from_reddit()
    pull_from_twitter()
    logger.info('finish')


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def corpus_age_limit_to_seconds():
    x = 60 * 60 * 24 * corpus_age_limit
    return x


def checked_log_age_limit_to_seconds():
    x = 60 * 60 * 24 * checked_logs_age_limit
    return x


def clean_corpus():
    path = 'corpus/'
    paths = [os.path.join(path, fname) for fname in os.listdir(path)]
    logger.debug('found {0} files in corpus'.format(len(paths)))
    for file in paths:
        m = os.path.getctime(file)  # could try os.path.getmtime()
        now = time.time()
        limit = now - corpus_age_limit_to_seconds()
        if m < limit:
            os.remove(file)
            logger.debug('removed {0} from corpus'.format(file))


def clean_logs():
    path = 'logs/'
    files = ['checked_reddit.txt', 'checked_twitter.txt']
    paths = [os.path.join(path, fname) for fname in files]
    for file in paths:
        m = os.path.getctime(file)  # could try os.path.getmtime()
        now = time.time()
        limit = now - checked_log_age_limit_to_seconds()
        if m < limit:
            os.remove(file)
            os.touch(file)
            logger.debug('refreshed {0}'.format(file))


def pull_from_reddit():
    with open('logs/checked_reddit.txt', 'r') as f:
        checked = f.read().splitlines()
        output = []
        for sub in subs:
            subreddit = reddit.subreddit(sub)
            for submission in subreddit.hot(limit=50):
                if submission.id not in checked:
                    # check on ups not implemented as pulling from .hot
                    # if submission.ups > somelimit
                    output.append(submission.title)
                    checked.append(submission.id)
    if len(output) == 0:
        print('No new submissions found')
        logger.info('no new submissions found')
    else:
        logger.info('found {0} submissions'.format(len(output)))
        output_filename = '{0}.txt'.format(uuid.uuid4().hex)
        logger.info('saving to {0}'.format(output_filename))
        with open('corpus/{0}'.format(output_filename), 'a') as f:
            for item in output:
                f.write(item + '\n')
    with open('logs/checked_reddit.txt', 'w') as f:
        for item in checked:
            f.write(item + '\n')


def pull_from_twitter():
    with open('logs/checked_twitter.txt', 'r') as f:
        checked = f.read().splitlines()
        output = []
        tweets = twitter.get_home_timeline()
        for t in tweets:
            if t['id_str'] not in checked:
                if not t['in_reply_to_status_id']:
                    tweet = t['text']
                    result = re.sub(r'http\S+', '', tweet)
                    output.append(result)
                    checked.append(t['id_str'])
    if len(output) == 0:
        print('No new submissions found')
        logger.info('no new submissions found')
    else:
        logger.info('found {0} submissions'.format(len(output)))
        output_filename = '{0}.txt'.format(uuid.uuid4().hex)
        logger.info('saving to {0}'.format(output_filename))
        with open('corpus/{0}'.format(output_filename), 'a') as f:
            for item in output:
                f.write(item + '\n')
    with open('logs/checked_twitter.txt', 'w') as f:
        for item in checked:
            f.write(item + '\n')


if __name__ == '__main__':
    main()
