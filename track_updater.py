import time
import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

URL = "https://systrum.net/"
OUTPUT_FILE = "now_playing.txt"
HISTORY_FILE = "history_log.txt"
DELAY = 10  # seconds

def setup_driver():
    options = Options()
    options.add_argument("--headless") 
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    return webdriver.Chrome(options=options)

def get_track(driver):
    try:
        driver.get(URL)
        time.sleep(3)

        marquees = driver.find_elements(By.CLASS_NAME, "auto-marquee")
        if len(marquees) < 2:
            return "RELAY//CONNECTING"

        artist = marquees[0].text.strip()
        title = marquees[1].text.strip()

        if not artist or not title:
            return "[Error] Empty"

        return f"{artist} {title}"
    except Exception as e:
        return f"[Error] {e}"

def main():
    driver = setup_driver()
    try:
        while True:
            track = get_track(driver)

            try:
                with open(OUTPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
                    current = f.read().strip()
            except FileNotFoundError:
                current = ""

            if track and track != current and not track.startswith("[Error]"):
                print(">>", track)

            # update track
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write(track)

            # track + timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{track} | {timestamp}"

            # check
            if not os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                    f.write(log_entry + "\n")
            else:
                with open(HISTORY_FILE, "r+", encoding="utf-8") as log:
                    all_lines = log.read().splitlines()
                    if not any(line.startswith(track) for line in all_lines):
                        log.write(log_entry + "\n")

            time.sleep(DELAY)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()