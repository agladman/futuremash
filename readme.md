# Futuremash 
A project to create a simple Twitter bot that uses Markov chains to generate fake tech news headlines.

## Main components

### corpusbuilder.py
This script uses PRAW to scrape headlines from various related subreddits and Twython to do the same from Twitter. Headlines are saved to text files in a `corpus` directory. Files older than 120 days are deleted in order to limit growth.

### tweetbuilder.py
This script uses the Markovify library to build the tweets from the files in the `corpus` directory.

At the moment output is just send to the command line, as the corpus is not yet large enough to build statisying sentences. Once this improves, tweetbuilder.py will use the Twitter API (via Twython) to send them out into the world.

## Development plans
- Explore hosting so the bot can be automated and run via cron jobs.
- Improve output with NLTK?
- Document dependencies.

### All the fake tech news that's fit to print to stdout
Here are some early favourites that have come up during testing:

- Twitter says it will ban diesel vehicles by 2025.
- Analysts predict Canada could have the stamina.
- AI learns to predict the future of government?
- The tech enabling a man rescuing a teeny kitten that wandered into traffic
- I just got real.