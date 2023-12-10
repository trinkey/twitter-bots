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
initial = int(input("How many minutes to wait to start sentence bot?\n>>> ")) * 60
secondary = int(input("How many minutes to wait to start birthday/emoji bot after sentence bot??\n>>> ")) * 60

def thread1():
    try:
        while True:
            time.sleep(1)
            logging.info("BIRTHDAY: [Re]starting thread...")
            subprocess.run(["python3", f"{abs_path}/birthdays/main.py"])
    except KeyboardInterrupt:
        exit()

def thread2():
    try:
        while True:
            time.sleep(1)
            logging.info("   WORDS: [Re]starting thread...")
            subprocess.run(["python3", f"{abs_path}/sentencebot/main.py"])
    except KeyboardInterrupt:
        exit()

def thread3():
    try:
        while True:
            time.sleep(1)
            logging.info("   EMOJI: [Re]starting thread...")
            subprocess.run(["python3", f"{abs_path}/emojibot/main.py"])
    except KeyboardInterrupt:
        exit()

th1 = threading.Thread(target=thread1)
th2 = threading.Thread(target=thread2)
th3 = threading.Thread(target=thread3)

time.sleep(initial)
th2.start()
time.sleep(secondary)
th1.start()
th3.start()

th1.join()
th2.join()
th3.join()
