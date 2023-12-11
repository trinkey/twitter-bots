import datetime
import requests
import logging
import json
import time

from requests_oauthlib import OAuth1
from oauth_tokens import *

prefix = "     EMOJI - "
abs_path = "/".join(__file__.replace("\\", "/").split("/")[:-1:])
logging.basicConfig(format=f"%(asctime)s: {prefix} %(message)s", datefmt="%H:%M:%S", level=logging.INFO)

emojiList = json.loads(open(f"{abs_path}/emoji.json", "r").read())

last = int(open(f"{abs_path}/info", "r").read().split("\n")[0])
index = int(open(f"{abs_path}/info", "r").read().split("\n")[1])

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
            logging.error("Network error!")
            exit()

        if response.status_code == 201:
            success = True
            logging.info("Sucessfully posted tweet!")
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
    now = str(datetime.datetime.now()).split(" ")[0].split("-")

    if int("".join(now)) > last:
        last = int("".join(now))

        postTweet("Emoji for Today: " + emojiList[index]["emoji"] + "\nEmoji name: " + emojiList[index]["name"].title().replace("\u229b ", ""))

        index += 1
        open(f"{abs_path}/info", "w").write(str(last) + "\n" + str(index))
        time.sleep(60 * 60 * 23 + 60 * 45) # 23h 45m

    else:
        time.sleep(60) # 1 minute polling until next day after original 23h 45m
