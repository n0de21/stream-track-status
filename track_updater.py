import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

URL = "https://systrum.net/"
OUTPUT_FILE = "now_playing.txt"
DELAY = 10  # секунд

def setup_driver():
    options = Options()
    options.add_argument("--headless")  # оставляем визуальный режим
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
            return "[Ошибка] Пустой текст"

        return f"{artist} {title}"
    except Exception as e:
        return f"[Ошибка] {e}"

def main():
    driver = setup_driver()
    try:
        while True:
            track = get_track(driver)

            # читаем, что в файле
            try:
                with open(OUTPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
                    current = f.read().strip()
            except FileNotFoundError:
                current = ""

            if track and track != current and not track.startswith("[Ошибка]"):
                print(">>", track)
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    f.write(track)

            time.sleep(DELAY)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()