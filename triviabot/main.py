import requests
import logging
import random
import base64
import time
import html

from requests_oauthlib import OAuth1
from oauth_tokens import *

abs_path = "/".join(__file__.replace("\\", "/").split("/")[:-1:])
logging.basicConfig(format="%(asctime)s: %(message)s", datefmt="%H:%M:%S", level=logging.INFO)

def postTweet(text):
    success = False
    while not success:
        try:
            response = requests.post(
                "https://api.twitter.com/2/tweets",
                auth=OAuth1(consumer_token, consumer_secret, access_token_trivia, access_secret_trivia),
                json={ "text": text },
                headers={ "Content-Type": "application/json" }
            )
        except:
            logging.error("    TRIVIA: Network error!")
            exit()

        if response.status_code == 201:
            success = True
            logging.info("    TRIVIA: Sucessfully posted tweet! Waiting 1h...")
        else:
            logging.info(f"    TRIVIA: Error posting tweet, status code {response.status_code}. Retrying in 30 seconds...")
            time.sleep(30)

while True:
    valid = False
    output = ""
    while not valid:
        time.sleep(5)
        x = requests.get(f"https://opentdb.com/api.php?amount=1&encode=base64&token={api_token}").json()["results"][0]
        q = [bytes.decode(base64.b64decode(i)) for i in x['incorrect_answers'] + [x['correct_answer']]]
        random.shuffle(q)
        output = html.unescape(f"Category: {bytes.decode(base64.b64decode(x['category'])).title()}\nDifficulty: {bytes.decode(base64.b64decode(x['difficulty'])).title()}\n\nQuestion: {'T/F - ' if bytes.decode(base64.b64decode(x['type'])) == 'boolean' else ''}{bytes.decode(base64.b64decode(x['question']))}\n{'Choices: ' + ', '.join(q) if bytes.decode(base64.b64decode(x['type'])) == 'multiple' else ''}\n\nAnswer: {bytes.decode(base64.b64decode(x['correct_answer']))}")
        valid = len(output) <= 280

    postTweet(output)

    time.sleep(60 * 60 - 6)
