# Gadgetech 
A project to create a simple Twitter bot that uses Markov chains to generate tech news headlines.
There will be two main components: corpusbuilder.py will use PRAW to scrape headlines from various related subreddits and tweetbuilder.py will use the Markovify library to build the tweets and the Twitter API (plus maybe Twython) to send them out into the world.