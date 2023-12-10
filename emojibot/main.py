import datetime
import requests
import logging
import json
import time

from requests_oauthlib import OAuth1
from oauth_tokens import *

logging.basicConfig(
    format="%(asctime)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S"
)

emojiList = json.loads(open("emoji.json", "r").read())

last = int(open("info", "r").read().split("\n")[0])
index = int(open("info", "r").read().split("\n")[1])

def postTweet(text):
    success = False

    while not success:
        try:
            response = requests.post(
                "https://api.twitter.com/2/tweets",
                auth=OAuth1(consumer_token, consumer_secret, access_token_emoji, access_secret_emoji),
                json={
                    "text": text
                },
                headers={
                    "Content-Type": "application/json"
                }
            )
        except:
            logging.error("   EMOJI: Network error!")
            exit()

        if response.status_code == 201:
            success = True
            logging.info("   EMOJI: Sucessfully posted tweet!")
        else:
            logging.info(f"   EMOJI: Error posting tweet, status code {response.status_code}. Retrying in 5 minutes...")
            time.sleep(60 * 5)

while True:
    now = str(datetime.datetime.now()).split(" ")[0].split("-")

    if int("".join(now)) > last:
        last = int("".join(now))

        postTweet("Emoji for Today: " + emojiList[index]["emoji"] + "\nEmoji name: " + emojiList[index]["name"].title().replace("\u229b ", ""))

        index += 1
        open("info", "w").write(str(last) + "\n" + str(index))
        time.sleep(60 * 60 * 23 + 60 * 45) # 23h 45m

    else:
        time.sleep(60) # 1 minute polling until next day after original 23h 45m
