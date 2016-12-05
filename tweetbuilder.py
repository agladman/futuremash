#!/usr/bin/env Python3

"""tweetbuilder.py: a script to generate and tweet fake tech news
    headlines using markov chains.

    For now output will just be sent to the command line.
    """

import logging.config
import markovify
import os
import yaml


log_cfg = yaml.load(open('config/logging.yml', 'r'))
logging.config.dictConfig(log_cfg)
logger = logging.getLogger(__name__)


def build_model():
    """builds the text model from files in the corpus folder"""
    submodels = []
    path = 'corpus/'
    files = [os.path.join(path, fname) for fname in os.listdir(path)]
    for i, file in enumerate(files):
        if file.endswith('.txt'):   # filter for OS junk like .DS_Store
            with open(file, 'r') as f:
                text = f.read()
                try:
                    i = markovify.Text(text)
                    submodels.append(i)
                except Exception as e:
                    logging.exception('exception creating submodel: ')
                    raise e
    logging.info('created {0} submodels'.format(len(submodels)))
    model = markovify.combine(submodels)
    logging.info('created combined model')
    return model


def test_output():
    """outputs 10 unqiue randomly-generated sentences of no more than 140
        characters
        """
    with open('logs/output_log.txt', 'r') as f:
        logged = f.read().splitlines()
    output = []
    while len(output) < 10:
        s = text_model.make_short_sentence(140)
        if s not in output:
            output.append(s)
    print('\n')
    new_to_log = []
    for i, s in enumerate(output):
        if s not in logged:
            new_to_log.append(s)
            print(i, s)
    with open('logs/output_log.txt', 'a') as f:
        for item in new_to_log:
            f.write(item + '\n')


if __name__ == '__main__':
    logging.info('start')
    text_model = build_model()
    test_output()
    logging.info('finish')
