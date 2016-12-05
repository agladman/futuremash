# Futuremash 
A project to create a simple Twitter bot that uses Markov chains to generate fake tech news headlines.

## Main components

### corpusbuilder.py
This script uses PRAW to scrape headlines from various related subreddits and Twython to do the same from Twitter. Headlines are saved to text files in a `corpus` directory. Files older than 120 days are deleted in order to limit growth.

### tweetbuilder.py
This script uses the Markovify library to build the tweets from the files in the `corpus` directory.

At the moment output is just send to the command line, as the corpus is not yet large enough to build statisying sentences. Once this improves, tweetbuilder.py will use the Twitter API (via Twython) to send them out into the world.

## Configuration
The scripts that make up Futuremash are built to read some configuration details from a file called `config.yml` which sits inside a `config` directory. It should be structured as follows:


```
reddit:
  my_user_agent: 'reddit user agent details'
  my_client_id: 'reddit client ID'
  my_client_secret: 'reddit client secret'
  my_username: 'reddit username'
  my_password: 'reddit password'
  
twitter:
  app_key: 'twitter app key'
  app_key_secret: 'twitter app secret'
  access_token: 'twitter access token'
  access_token_secret: 'twitter access token secret'

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
- Think about a way of adding images to some tweets at some point.
- Explore hosting so the bot can be automated and run via cron jobs.
- Control growth of config files checked_reddit.txt,  checked_twitter.txt and output_log.txt.
- Improve output with NLTK?
- Document dependencies.

### All the fake tech news that's fit to print to stdout
Here are some early favourites that have come up during testing:

- Twitter says it will ban diesel vehicles by 2025.
- Analysts predict Canada could have the stamina.
- AI learns to predict the future of government?
- The tech enabling a man rescuing a teeny kitten that wandered into traffic