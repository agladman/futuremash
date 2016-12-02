#!/usr/bin/env Python3

"""tweetbuilder.py: a script to generate and tweet fake tech news
    headlines using markov chains.

    For now output will just be sent to the command line.
    """


import markovify
import os


def build_model():
    """builds the text model from files in the corpus folder"""
    submodels = []
    path = 'corpus/'
    files = [os.path.join(path, fname) for fname in os.listdir(path)]
    for i, file in enumerate(files):
        with open(file, 'r') as f:
            text = f.read()
        i = markovify.Text(text)
        submodels.append(i)
    model = markovify.combine(submodels)
    return model


def test_output():
    """prints 10 unqiue randomly-generated sentences of no more than 140
        characters
        """
    output = []
    while len(output) < 10:
        s = text_model.make_short_sentence(140)
        if s not in output:
            output.append(s)
    print('\n')
    for s in output:
        print(s)


if __name__ == '__main__':
    text_model = build_model()
    test_output()
