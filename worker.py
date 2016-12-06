#!/usr/bin/env Python3

"""crappy docstring"""


import corpusbuilder
import logging.config
import random
import time
import tweetbuilder
import yaml


log_cfg = yaml.load(open('config/logging.yml', 'r'))
logging.config.dictConfig(log_cfg)
logger = logging.getLogger(__name__)


def get_command(object):
    commands = (object.tweet,
                object.tweet_with_image,
                try_corpus)
    c = random.choice(commands)
    logger.info(c)
    return c


def try_corpus():
    try:
        corpusbuilder.main()
    except Exception:
        logger.exception('failed to extend corpus')
        pass


def main():
    try:
        t = tweetbuilder.Tweeter()
        logger.info('Tweeter created')
    except Exception:
        logger.exception('failed to create Tweeter')

    while t:
        get_command(t)()
        zzz = random.randint(300, 900)   # usually 5400, 14400
        logger.info('sleeping {0}'.format(zzz))
        time.sleep(zzz)    # min 30 mins between tweets


if __name__ == '__main__':
    try:
        main()
    except ConnectionResetError:
        logger.exception('worker.py stopped: ')
        pass  
