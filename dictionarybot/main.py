import requests
import logging
import json
import time

from requests_oauthlib import OAuth1
from oauth_tokens import *

prefix = "DICTIONARY - "
abs_path = "/".join(__file__.replace("\\", "/").split("/")[:-1:])
words = json.loads(open(f"{abs_path}/dictionary.json", "r").read())
index = int(open(f"{abs_path}/info", "r").read())
logging.basicConfig(format=f"%(asctime)s: {prefix} %(message)s", datefmt="%H:%M:%S", level=logging.INFO)

def postTweet(text):
    success = False
    while not success:
        try:
            response = requests.post(
                "https://api.twitter.com/2/tweets",
                auth=OAuth1(consumer_token, consumer_secret, access_token_dictionary, access_secret_dictionary),
                json={ "text": text },
                headers={ "Content-Type": "application/json" }
            )
        except:
            logging.error("Network error!")
            exit()

        if response.status_code == 201:
            success = True
            logging.info("Sucessfully posted tweet! Waiting 1h...")
        elif response.status_code == 429:
            logging.info("Rate limited! Trying again in 1h...")
            time.sleep(60 * 60)
        elif response.status_code == 403:
            success = True
            logging.info("Duplicate tweet! (probably)")
        else:
            logging.info(f"Error posting tweet, status code {response.status_code}. Retrying in 30 seconds...")
            time.sleep(30)

while True:
    postTweet(f"{words[index]['word'].title()}: {words[index]['definition']}")

    index += 1
    f = open(f"{abs_path}/info", "w")
    f.write(str(index))
    f.close()

    time.sleep(60 * 60)
