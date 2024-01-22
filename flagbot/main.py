import requests
import logging
import random
import json
import time

from requests_oauthlib import OAuth1
from oauth_tokens import *

prefix = "      FLAG - "
abs_path = "/".join(__file__.replace("\\", "/").split("/")[:-1:])
logging.basicConfig(format=f"%(asctime)s: {prefix} %(message)s", datefmt="%H:%M:%S", level=logging.INFO)

flag_list = json.loads(open(f"{abs_path}/emoji.json", "r").read())
index = int(open(f"{abs_path}/info", "r").read())

def postTweet(text, poll_data):
    success = False

    while not success:
        try:
            response = requests.post(
                "https://api.twitter.com/2/tweets",
                auth=OAuth1(consumer_token, consumer_secret, access_token_flag, access_secret_flag),
                json={
                    "text": text,
                    "poll": {
                        "options": poll_data,
                        "duration_minutes": 60 * 24 # 24 hours
                    }
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
            logging.info(f"Error posting tweet, status code {response.status_code}: {response.text}. Retrying in 30 seconds...")
            time.sleep(30)

while True:
    choices = [random.randint(1, len(flag_list)) - 1]
    for i in range(3):
        first = True
        while first or choice in choices:
            first = False
            choice = random.randint(1, len(flag_list)) - 1
        choices.append(choice)

    x = choices[0]
    random.shuffle(choices)

    postTweet(
        f"Guess the Flag #{index}! Which of the following is {flag_list[x]['name'].upper()}?",
        poll_data=[
            flag_list[choices[0]]["emoji"],
            flag_list[choices[1]]["emoji"],
            flag_list[choices[2]]["emoji"],
            flag_list[choices[3]]["emoji"]
        ]
    )

    del choices
    index += 1
    open(f"{abs_path}/info", "w").write(str(index))
    time.sleep(60 * 60)
