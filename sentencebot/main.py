import requests
import logging
import random
import time

from requests_oauthlib import OAuth1
from oauth_tokens import *

abs_path = "/".join(__file__.replace("\\", "/").split("/")[:-1:])
words = open(f"{abs_path}/words.txt", "r").read().split("\n")
logging.basicConfig(format="%(asctime)s: %(message)s", datefmt="%H:%M:%S", level=logging.INFO)

def postTweet(text):
    success = False
    while not success:
        try:
            response = requests.post(
                "https://api.twitter.com/2/tweets",
                auth=OAuth1(consumer_token, consumer_secret, access_token_words, access_secret_words),
                json={ "text": text },
                headers={ "Content-Type": "application/json" }
            )
        except:
            logging.error("     WORDS: Network error!")
            exit()

        if response.status_code == 201:
            success = True
            logging.info("     WORDS: Sucessfully posted tweet! Waiting 1h...")
        else:
            logging.info(f"     WORDS: Error posting tweet, status code {response.status_code}. Retrying in 30 seconds...")
            time.sleep(30)

while True:
    output = []
    for i in range(random.randint(4, 14)):
        output.append(random.choice(words))
    stringOutput = " ".join(output) + "."
    postTweet(stringOutput[:1:].upper() + stringOutput[1::])

    time.sleep(60 * 60)
