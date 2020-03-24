import os
from dotenv import load_dotenv
import twitter
import imggen

"""
Running this file will produce one tweet. I use cron to schedule regular tweets.
"""
load_dotenv()

api = twitter.Api(consumer_key = os.getenv('CONSUMER_KEY'),
                  consumer_secret = os.getenv('CONSUMER_SECRET'),
                  access_token_key = os.getenv('ACCESS_TOKEN_KEY'),
                  access_token_secret = os.getenv('ACCESS_TOKEN_SECRET'))
imggen.make_meme('img.png')
with open('img.png', 'rb') as img:
    api.PostUpdate('', media=img)
