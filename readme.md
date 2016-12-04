# Gadgetech 
A project to create a simple Twitter bot that uses Markov chains to generate fake tech news headlines.

## Main components
- corpusbuilder.py uses PRAW to scrape headlines from various related subreddits.
- tweetbuilder.py uses the Markovify library to build the tweets.

At the moment output is just send to the command line, as the corpus is not yet large enough to build statisying sentences. Once this improves, tweetbuilder.py will use the Twitter API (plus/or maybe Twython) to send them out into the world.

## Configuring Gadgetech
The scripts that make up Gadgetech are built to read some configuration details from a file called `config.yml` which sits inside a `config` directory. It should be structured as follows:


```
reddit:
  my_user_agent: 'reddit user agent details'
  my_client_id: 'reddit client ID'
  my_client_secret: 'reddit client secret'
  my_username: 'reddit username'
  my_password: 'reddit password'

age:
  corpus_age_limit_days: 120	# max age of corpus files in days

subreddits:
  - 'list'
  - 'of'
  - 'subreddits'
  - 'to_fetch'
  - 'headlines'
  - 'from'
 
```

## Development plans
- Integrate Twitter via its API and/or the Twython library.
- Think about a way of adding images to some tweets at some point.
- Explore hosting so the bot can be automated and run via cron jobs.
- Extend corpusbuilder.py to take in material from Twitter feeds.
- Log sent tweets to the bot doesn't repeat itself
- Control growth of checked.txt

### All the fake tech news that's fit to print to stdout
Here are some early favourites that have come up during testing:

- Twitter says it will ban diesel vehicles by 2025.
- Charging Your Phone in Seconds and the GOP may be caused by gut bacteria.
- Relax, artificial intelligence isn’t coming for your 2016 MacBook Pro?
- Wearable device for tablets.