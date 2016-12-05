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


def build_tweet(text_model, length=140):
    return text_model.make_short_sentence(length)


def test_output(text_model):
    """Outputs 10 unqiue randomly-generated sentences of no more than 140
        characters.
        """
    with open('logs/output_log.txt', 'r') as f:
        logged = f.read().splitlines()
    output = []
    while len(output) < 10:
        s = build_tweet(text_model, 120)
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
