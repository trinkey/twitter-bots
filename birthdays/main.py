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

last = int(open("info", "r").read())
monthMap = {
    "01": "Jan.", "02": "Feb.", "03": "Mar.",
    "04": "Apr.", "05": "May",  "06": "Jun.",
    "07": "Jul.", "08": "Aug.", "09": "Sep.",
    "10": "Oct.", "11": "Nov.", "12": "Dec."
}

def postTweet(text):
    success = False

    while not success:
        try:
            response = requests.post(
                "https://api.twitter.com/2/tweets",
                auth=OAuth1(consumer_token, consumer_secret, access_token_birthday, access_secret_birthday),
                json={
                    "text": text
                },
                headers={
                    "Content-Type": "application/json"
                }
            )
        except:
            logging.error("BIRTHDAY: Network error!")
            exit()

        if response.status_code == 201:
            success = True
            logging.info("BIRTHDAY: Sucessfully posted tweet!")
        else:
            logging.info(f"BIRTHDAY: Error posting tweet, status code {response.status_code}. Retrying in 5 minutes...")
            time.sleep(60 * 5)

while True:
    now = str(datetime.datetime.now()).split(" ")[0].split("-")

    if int("".join(now)) > last:
        last = int("".join(now))

        try:
            f = json.loads(requests.get(f"https://{SECRET_URL}/birthdays.json").text)
        except:
            logging.error("BIRTHDAY: Network error!")
            exit()
        birthdays = []

        for i in f:
            if int("".join(now)[4::]) == i["date"]:
                birthdays.append(i["name"])

        if birthdays:
            postTweet(f"Today is {monthMap[now[1]]} {now[2]}, make sure to wish a happy birthday to {(', '.join(birthdays[:-1]) + (',' if len(birthdays) >= 3 else '') + ' and ' if len(birthdays) >= 2 else '') + birthdays[-1]}!!!")
        else:
            postTweet(f"There are no birthdays for today ({monthMap[now[1]]} {now[2]}) in my database!\nIf today is your birthday, or you want to be added to the pool of birthdays, you can dm this account or @trinkey_2!")

        open("info", "w").write(str(last))
        time.sleep(60 * 60 * 23 + 60 * 45) # 23h 45m

    else:
        time.sleep(60) # 1 minute polling until next day after original 23h 45m
