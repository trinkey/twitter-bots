print("Initializing...")

import threading
import datetime
import requests
import base64
import random
import time
import json
import html
import os

from requests_oauthlib import OAuth1
from datetime import datetime

from oauth_tokens import *

abs_path = "/".join(__file__.replace("\\", "/").split("/")[:-1:])

if not os.path.exists(f"{abs_path}/save"):
    os.mkdir(f"{abs_path}/save")
elif not os.path.isdir(f"{abs_path}/save"):
    os.remove(f"{abs_path}/save")
    os.mkdir(f"{abs_path}/save")

def ensure(path, default):
    if not os.path.exists(f"{abs_path}/{path}"):
        open(f"{abs_path}/{path}", "w").write(default)

ensure("save/info_birthday", "0")
ensure("save/info_emoji", "0\n0")
ensure("save/info_dict", "0")
ensure("save/info_flag", "1")
ensure("save/info_counting", "1")
ensure("save/info_emojiguess", "1")
ensure("save/info_wiki_todo", "")
ensure("save/info_wiki_done", "")

words = open(f"{abs_path}/storage/words.txt", "r").read().split("\n")
emoji_list = json.loads(open(f"{abs_path}/storage/emoji.json", "r").read())
dct = json.loads(open(f"{abs_path}/storage/dictionary.json", "r").read())
flag_list = json.loads(open(f"{abs_path}/storage/flags.json", "r").read())

monthMap = {
    "01": "Jan.", "02": "Feb.", "03": "Mar.",
    "04": "Apr.", "05": "May",  "06": "Jun.",
    "07": "Jul.", "08": "Aug.", "09": "Sep.",
    "10": "Oct.", "11": "Nov.", "12": "Dec."
}

def log(msg, prefix=""):
    print(f"{prefix}{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - {msg}")

def error(err, prefix=""):
    print(f"\x1b[38;5;9m{prefix}{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - \x1b[0;0m{err}")

def warn(err, prefix=""):
    print(f"\x1b[38;5;3m{prefix}{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - \x1b[0;0m{err}")

def postTweet(text, oauth, prefix, poll_info=None, time_str="some amount of time"):
    success = False

    while not success:
        try:
            response = requests.post(
                "https://api.twitter.com/2/tweets",
                auth=OAuth1(*oauth),
                json={
                    "text": text
                } if not poll_info else {
                    "text": text,
                    "poll": {
                        "options": poll_info,
                        "duration_minutes": 60 * 24 # 24 hours
                    }
                },
                headers={
                    "Content-Type": "application/json"
                }
            )
        except:
            error("Network error!", prefix)
            break

        if response.status_code == 201:
            success = True
            log(f"Sucessfully posted tweet! Waiting {time_str}...", prefix)
        elif response.status_code == 429:
            error("Rate limited! Trying again in 1h...", prefix)
            time.sleep(60 * 60)
        elif response.status_code == 403:
            success = True
            error("Duplicate tweet! (probably)", prefix)
        else:
            error(f"Error posting tweet, status code {response.status_code}. Retrying in 30 seconds...", prefix)
            time.sleep(30)

def open_list(path, split: str="\n", default: list[str]=[]) -> list[str]:
    f = open(path, "r").read()
    if f:
        return f.split(split)
    return default

def th_birthday():
    prefix = "  BIRTHDAY - "
    log("Starting thread", prefix)
    oauth = [consumer_token_trinkey_2, consumer_secret_trinkey_2, access_token_birthday, access_secret_birthday]
    last = int(open(f"{abs_path}/save/info_birthday", "r").read())

    while True:
        now = str(datetime.now()).split(" ")[0].split("-")

        if int("".join(now)) > last:
            last = int("".join(now))

            try:
                f = json.loads(requests.get(f"https://{SECRET_URL}/birthdays.json").text)
            except:
                error("Network error!", prefix)
                continue

            birthdays = []

            for i in f:
                if int("".join(now)[4::]) == i["date"]:
                    birthdays.append(i["name"])

            if birthdays:
                postTweet(f"Today is {monthMap[now[1]]} {now[2]}, {now[0]}, make sure to wish a happy birthday to {(', '.join(birthdays[:-1]) + (',' if len(birthdays) >= 3 else '') + ' and ' if len(birthdays) >= 2 else '') + birthdays[-1]}!!!", oauth, prefix, time_str="24h")
            else:
                postTweet(f"There are no birthdays for today ({monthMap[now[1]]} {now[2]}, {now[0]}) in my database!\nIf today is your birthday, or you want to be added to the pool of birthdays, submit it at https://birthdays.pythonanywhere.com!", oauth, prefix, time_str="24h")

            open(f"{abs_path}/save/info_birthday", "w").write(str(last))
            time.sleep(60 * 60 * 23 + 60 * 45) # 23h 45m

        else:
            time.sleep(60) # 1 minute polling until next day after original 23h 45m

def th_sentences():
    prefix = "  SENTENCE - "
    log("Starting thread", prefix)
    oauth = [consumer_token_trinkey_, consumer_secret_trinkey_, access_token_words, access_secret_words]

    while True:
        output = []
        for _ in range(random.randint(4, 14)):
            output.append(random.choice(words))

        stringOutput = " ".join(output) + "."
        postTweet(stringOutput[:1:].upper() + stringOutput[1::], oauth, prefix, time_str="1h")

        time.sleep(60 * 60)

def th_emoji():
    prefix = "     EMOJI - "
    log("Starting thread", prefix)
    oauth = [consumer_token_trinkey_2, consumer_secret_trinkey_2, access_token_emoji, access_secret_emoji]

    last, index = [int(i) for i in open(f"{abs_path}/save/info_emoji", "r").read().split("\n")]

    while True:
        now = str(datetime.now()).split(" ")[0].split("-")

        if int("".join(now)) > last:
            last = int("".join(now))

            postTweet("Emoji for Today: " + emoji_list[index]["emoji"] + "\nEmoji name: " + emoji_list[index]["name"].title().replace("\u229b ", ""), oauth, prefix, time_str="24h")

            index += 1
            open(f"{abs_path}/save/info_emoji", "w").write(str(last) + "\n" + str(index))
            time.sleep(60 * 60 * 23 + 60 * 45) # 23h 45m

        else:
            time.sleep(60) # 1 minute polling until next day after original 23h 45m

def th_dictionary():
    prefix = "DICTIONARY - "
    log("Starting thread", prefix)
    oauth = [consumer_token_trinkey_2, consumer_secret_trinkey_2, access_token_dictionary, access_secret_dictionary]

    index = int(open(f"{abs_path}/save/info_dict", "r").read())

    while True:
        postTweet(f"{dct[index]['word'].title()}: {dct[index]['definition']}", oauth, prefix, time_str="1h")

        index += 1
        f = open(f"{abs_path}/save/info_dict", "w")
        f.write(str(index))
        f.close()

        time.sleep(60 * 60)

def th_trivia():
    prefix = "    TRIVIA - "
    log("Starting thread", prefix)
    oauth = [consumer_token_trinkey_, consumer_secret_trinkey_, access_token_trivia, access_secret_trivia]

    while True:
        valid = False
        output = ""
        count = 0

        while not valid:
            time.sleep(5) # Prevent ratelimit / 1 request/5s/ip
            count += 1
            try:
                x = requests.get(f"https://opentdb.com/api.php?amount=1&encode=base64").json()["results"][0]
            except:
                error("Network error!", prefix)
                continue

            q = [bytes.decode(base64.b64decode(i)) for i in x['incorrect_answers'] + [x['correct_answer']]]
            random.shuffle(q)
            output = html.unescape(f"Category: {bytes.decode(base64.b64decode(x['category'])).title()}\nDifficulty: {bytes.decode(base64.b64decode(x['difficulty'])).title()}\n\nQuestion: {'T/F - ' if bytes.decode(base64.b64decode(x['type'])) == 'boolean' else ''}{bytes.decode(base64.b64decode(x['question']))}\n{'Choices: ' + ', '.join(q) if bytes.decode(base64.b64decode(x['type'])) == 'multiple' else ''}\n\nAnswer (b64 encoded): {x['correct_answer']}")
            valid = len(output) <= 280

        postTweet(output, oauth, prefix, time_str="1h")

        time.sleep(60 * 60 - 5 * count)

def th_flag():
    prefix = "      FLAG - "
    log("Starting thread", prefix)
    oauth = [consumer_token_trinkey_2, consumer_secret_trinkey_2, access_token_flag, access_secret_flag]

    index = int(open(f"{abs_path}/save/info_flag", "r").read())

    while True:
        choices = []
        for _ in range(4):
            first = True
            choice = -1
            while first or choice in choices:
                first = False
                choice = random.randint(1, len(flag_list)) - 1
            choices.append(choice)

        x = random.choice(choices)
        random.shuffle(choices)

        if random.randint(0, 1):
            postTweet(
                f"Guess the Flag #{index}! Which of the following is {flag_list[x]['name'].upper()}?",
                oauth, prefix,
                poll_info=[
                    flag_list[choices[0]]["emoji"],
                    flag_list[choices[1]]["emoji"],
                    flag_list[choices[2]]["emoji"],
                    flag_list[choices[3]]["emoji"]
                ], time_str="1h"
            )
        else:
            postTweet(
                f"Guess the Flag #{index}! What country has the flag {flag_list[x]['emoji']}?",
                oauth, prefix,
                poll_info=[
                    flag_list[choices[0]]["name"],
                    flag_list[choices[1]]["name"],
                    flag_list[choices[2]]["name"],
                    flag_list[choices[3]]["name"]
                ], time_str="1h"
            )

        index += 1
        open(f"{abs_path}/save/info_flag", "w").write(str(index))
        time.sleep(60 * 60)

def th_counting():
    prefix = "  COUNTING - "
    log("Starting thread", prefix)
    oauth = [consumer_token__trinkey, consumer_secret__trinkey, access_token_counting, access_secret_counting]

    count = int(open(f"{abs_path}/save/info_counting", "r").read())

    while True:
        postTweet(str(count), oauth, prefix, time_str="30m")

        count += 1
        f = open(f"{abs_path}/save/info_counting", "w")
        f.write(str(count))
        f.close()

        time.sleep(60 * 30)

def th_emojiguess():
    prefix = "EMOJIGUESS - "
    log("Starting thread", prefix)
    oauth = [consumer_token_GuessThatEmoji, consumer_secret_GuessThatEmoji, access_token_emojiguess, access_secret_emojiguess]

    index = int(open(f"{abs_path}/save/info_emojiguess", "r").read())

    while True:
        choices = []
        for _ in range(4):
            first = True
            choice = -1
            while first or choice in choices:
                first = False
                choice = random.randint(1, len(emoji_list)) - 1
            choices.append(choice)

        x = random.choice(choices)
        random.shuffle(choices)

        if random.randint(0, 1):
            postTweet(
                f"Guess the Emoji #{index}! What is the correct name for {emoji_list[x]['name'].upper()}?",
                oauth, prefix,
                poll_info=[
                    emoji_list[choices[0]]["emoji"],
                    emoji_list[choices[1]]["emoji"],
                    emoji_list[choices[2]]["emoji"],
                    emoji_list[choices[3]]["emoji"]
                ], time_str="1h"
            )
        else:
            while len(emoji_list[choices[0]]["name"]) > 25 or len(emoji_list[choices[1]]["name"]) > 25 or len(emoji_list[choices[2]]["name"]) > 25 or len(emoji_list[choices[3]]["name"]) > 25:
                choices = []
                for _ in range(4):
                    first = True
                    choice = -1
                    while first or choice in choices:
                        first = False
                        choice = random.randint(1, len(emoji_list)) - 1
                    choices.append(choice)

                x = random.choice(choices)
                random.shuffle(choices)

            postTweet(
                f"Guess the Emoji #{index}! What is {emoji_list[x]['emoji']} called?",
                oauth, prefix,
                poll_info=[
                    emoji_list[choices[0]]["name"],
                    emoji_list[choices[1]]["name"],
                    emoji_list[choices[2]]["name"],
                    emoji_list[choices[3]]["name"]
                ], time_str="1h"
            )

        index += 1
        open(f"{abs_path}/save/info_emojiguess", "w").write(str(index))
        time.sleep(60 * 60)

def th_wiki():
    prefix = " WIKIPEDIA - "
    oauth = []

    todo = open_list("todo.txt")
    done = open_list("complete.txt")

    stupid = False
    stupid2 = False

    while True:
        try:
            stupid = False
            stupid2 = False
            if len(todo):
                stupid = True
                response = requests.get(f"https://en.wikipedia.org{todo[0]}")
                base_url = todo.pop(0)
                stupid = False
            else:
                response = requests.get("https://en.wikipedia.org/wiki/Special:Random")
                base_url = "/wiki/" + response.text.split('<link rel="canonical" href="', 1)[1].split("\"", 1)[0].split("/wiki/", 1)[1]

            stupid2 = True
            done.append(base_url)
            text = response.text.split('id="firstHeading"', 1)[1].split('id="External_links"', 1)[0]
            for i in text.split('href="/wiki/')[1::]:
                if ":" in i and i.split(":")[0] in [
                    "Special", "Help", "File", "Talk", "Wikipedia", "Category", "Template", "Module"
                ]:  continue

                QUOT = "\""
                link = f"/wiki/{i.split(QUOT, 1)[0]}"
                if link not in todo and link not in done:
                    todo.append(link)

                if len(todo) >= 25:
                    break

            postTweet(html.unescape(f"{response.text.split('<title', 1)[1].split('>', 1)[1].split(' - Wikipedia</title>', 1)[0].split('</', 1)[0]}\nhttps://en.wikipedia.org{base_url}"), oauth, prefix)

            time.sleep(60 * 60)

        except KeyboardInterrupt:
            exit()

        except BaseException as e:
            if stupid2:
                done.pop(-1)
            if stupid:
                todo.pop(0)
            error(f"Err {e}, retrying...")

        open(f"{abs_path}/save/info_wiki_done", "w").write("\n".join(done))
        open(f"{abs_path}/save/info_wiki_todo", "w").write("\n".join(todo))


print("To stop, press Ctrl+C any time.")
count = float(input("How many minutes to wait until starting bi-hourly bots?\n>>> ")) * 60
initial = float(input("How many minutes to wait after that to start hourly bots?\n>>> ")) * 60
secondary = float(input("How many minutes to wait after those to start daily bots?\n>>> ")) * 60

birthday   = threading.Thread(target=th_birthday)
sentences  = threading.Thread(target=th_sentences)
emojibot   = threading.Thread(target=th_emoji)
dictionary = threading.Thread(target=th_dictionary)
triviabot  = threading.Thread(target=th_trivia)
flagbot    = threading.Thread(target=th_flag)
counting   = threading.Thread(target=th_counting)
emojiguess = threading.Thread(target=th_emojiguess)
wiki       = threading.Thread(target=th_wiki)

time.sleep(count)
counting.start()

time.sleep(initial)
triviabot.start()
sentences.start()
flagbot.start()
dictionary.start()
emojiguess.start()
wiki.start()

time.sleep(secondary)
birthday.start()
emojibot.start()

birthday.join()
sentences.join()
emojibot.join()
dictionary.join()
triviabot.join()
flagbot.join()
counting.join()
emojiguess.join()
wiki.join()
