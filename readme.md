# Gadgetech 
A project to create a simple Twitter bot that uses Markov chains to generate fake tech news headlines.

## Main components
- corpusbuilder.py uses PRAW to scrape headlines from various related subreddits.
- tweetbuilder.py uses the Markovify library to build the tweets.

At the moment output is just send to the command line, as the corpus is not yet large enough to build statisying sentences. Once this improves, tweetbuilder.py will use the Twitter API (plus/or maybe Twython) to send them out into the world.

## Development plans
- Integrate Twitter via its API and/or the Twython library.
- Think about a way of adding images to some tweets at some point.
- Explore hosting so the bot can be automated and run via cron jobs.
- Extend corpusbuilder.py to take in material from Twitter feeds.

## All the fake tech news that's fit to print to stdout
Here are some early favourites that have come up during testing:
- Wearable device for tablets.
- Twitter says it will ban diesel vehicles by 2025.