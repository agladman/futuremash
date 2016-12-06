#!/usr/bin/env Python3

"""tweetbuilder.py: a script to generate and tweet fake tech news
    headlines using markov chains.

    For now output will just be sent to the command line.
    """

import logging.config
import markovify
import os
from random import choice
from twython import Twython
import yaml


log_cfg = yaml.load(open('config/logging.yml', 'r'))
logging.config.dictConfig(log_cfg)
logger = logging.getLogger(__name__)


class Tweeter(object):
    """docstring for Tweeter"""
    def __init__(self, name):
        super(Tweeter, self).__init__()
        self.name = name
        self.APP_KEY = None
        self.APP_SECRET = None
        self.OAUTH_TOKEN = None
        self.OAUTH_TOKEN_SECRET = None
        self.tweet_length = 140
        self.config(self)
        self.twitter = Twython(self.APP_KEY,
                               self.APP_SECRET,
                               self.OAUTH_TOKEN,
                               self.OAUTH_TOKEN_SECRET)
        self.text_model = build_model()

    def config(self):
        # read from config file and set variables
        with open('config.yml', 'r') as f:
            try:
                cfg = yaml.load(f)
            except yaml.YAMLError as exc:
                print(exc)

        if cfg:
            self.APP_KEY = cfg['twitter']['app_key']
            self.APP_SECRET = cfg['twitter']['app_key_secret']
            self.OAUTH_TOKEN = cfg['twitter']['access_token']
            self.OAUTH_TOKEN_SECRET = cfg['twitter']['access_token_secret']
            self.tweet_length = cfg['twitter']['tweet_length']

    def build_tweet(self):
        with open('logs/output_log.txt', 'r') as f:
            logged = f.read().splitlines()
        unique = False
        while not unique:
            tweet = self.text_model.make_short_sentence(self.tweet_length)
            if tweet not in logged:
                logged.append(tweet)
                unique = True
        with open('logs/output_log.txt', 'w') as f:
            for item in logged:
                f.write(item + '\n')
        return tweet

    def choose_media(self):
        path = 'media/'
        paths = [os.path.join(path, fname) for fname in os.listdir(path)]
        return choice(paths)

    def tweet(self):
        self.twitter.update_status(status=self.build_tweet())

    def tweet_with_image(self):
        photo = self.choose_media()
        text = self.build_tweet()
        with open(photo, 'rb') as p:
            response = self.twitter.upload_media(media=p)
        self.twitter.update_status(
            status=text, media_ids=[response['media_id']])
        os.remove(photo)


def main():
    logger.info('start')
    text_model = build_model()
    if text_model:
        test_output(text_model)
    else:
        print('I have nothing to say right now.')
    logger.info('finish')


def build_model():
    """Builds the text model from files in the corpus folder by looping
        over all files and creating a submodel for each file and finally
        combining these into one.
        """
    submodels = []
    path = 'corpus/'
    files = [os.path.join(path, fname) for fname in os.listdir(path)]
    for i, file in enumerate(files):
        if file.endswith('.txt'):   # filter for OS junk like .DS_Store
            with open(file, 'r') as f:
                text = f.read()
                logging.debug('reading {0}'.format(file))
                logging.debug('type passed to corpus: {0}'.format(type(text)))
                logging.debug('text: {0}'.format(text))
                try:
                    i = markovify.Text(text)
                    submodels.append(i)
                except Exception:
                    logging.exception('exception creating submodel: ')
                    # TODO: automatically move files that throw
                    # UnicodeDecodeError to another dir
                    pass
    logger.info('created {0} submodels'.format(len(submodels)))
    if len(submodels) > 0:
        model = markovify.combine(submodels)
        logger.info('created combined model')
        return model
    else:
        logger.error('unable to create text model')
        return False


def test_output(text_model):
    """Outputs 10 unqiue randomly-generated sentences of no more than 140
        characters.
        """
    with open('logs/output_log.txt', 'r') as f:
        logged = f.read().splitlines()
    output = []
    while len(output) < 10:
        s = text_model.make_short_sentence(120)
        if s not in output:
            output.append(s)
    print('\n')
    for i, s in enumerate(output):
        if s not in logged:
            logged.append(s)
            print(i, s)
    with open('logs/output_log.txt', 'w') as f:
        for item in logged:
            f.write(item + '\n')


if __name__ == '__main__':
    main()
