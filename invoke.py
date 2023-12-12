import subprocess
import threading
import logging
import time

abs_path = "/".join(__file__.replace("\\", "/").split("/")[:-1:])

logging.basicConfig(
    format="%(asctime)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S"
)

print("To stop, press Ctrl+C any time.")
initial = int(input("How many minutes to wait to start sentence/dictionary/trivia bot?\n>>> ")) * 60
secondary = int(input("How many minutes to wait to start birthday/emoji bot after sentence bot??\n>>> ")) * 60

def thread1():
    try:
        while True:
            time.sleep(1)
            logging.info("  BIRTHDAY - [Re]starting thread...")
            subprocess.run(["python3", f"{abs_path}/birthdays/main.py"])
    except KeyboardInterrupt:
        exit()

def thread2():
    try:
        while True:
            time.sleep(1)
            logging.info("     WORDS - [Re]starting thread...")
            subprocess.run(["python3", f"{abs_path}/sentencebot/main.py"])
    except KeyboardInterrupt:
        exit()

def thread3():
    try:
        while True:
            time.sleep(1)
            logging.info("     EMOJI - [Re]starting thread...")
            subprocess.run(["python3", f"{abs_path}/emojibot/main.py"])
    except KeyboardInterrupt:
        exit()

def thread4():
    try:
        while True:
            time.sleep(1)
            logging.info("DICTIONARY - [Re]starting thread...")
            subprocess.run(["python3", f"{abs_path}/dictionarybot/main.py"])
    except KeyboardInterrupt:
        exit()

def thread5():
    try:
        while True:
            time.sleep(1)
            logging.info("    TRIVIA - [Re]starting thread...")
            subprocess.run(["python3", f"{abs_path}/triviabot/main.py"])
    except KeyboardInterrupt:
        exit()

# 1 - birthday
# 2 - sentences
# 3 - emoji
# 4 - dictionary
# 5 - trivia

birthday = threading.Thread(target=thread1)
sentences = threading.Thread(target=thread2)
emojibot = threading.Thread(target=thread3)
dictionary = threading.Thread(target=thread4)
triviabot = threading.Thread(target=thread5)

time.sleep(initial - 5)
triviabot.start()
time.sleep(5)
sentences.start()
dictionary.start()
time.sleep(secondary)
birthday.start()
emojibot.start()

birthday.join()
sentences.join()
emojibot.join()
dictionary.join()
triviabot.join()
