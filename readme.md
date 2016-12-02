# Gadgetech 
A project to create a simple Twitter bot that uses Markov chains to generate tech news headlines.

There are two main components: corpusbuilder.py uses PRAW to scrape headlines from various related subreddits and tweetbuilder.py uses the Markovify library to build the tweets.

At the moment output is just send to the command line, as the corpus is not yet large enough to build statisying sentences. Once this improves, tweetbuilder.py will use the Twitter API (plus/or maybe Twython) to send them out into the world.

I may think about a way of adding images to some tweets at some point.