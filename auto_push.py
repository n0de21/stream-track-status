import os
import time
from git import Repo

REPO_PATH = r"C:\Users\user\Documents\GitHub\stream-track-status"
FILENAME = "now_playing.txt"
FULL_PATH = os.path.join(REPO_PATH, FILENAME)
CHECK_DELAY = 30

def push_update(repo_path, file_name):
    repo = Repo(repo_path)
    repo.git.add(file_name)
    repo.index.commit("track update")
    origin = repo.remote(name="origin")
    origin.push()

def main():
    last_content = ""
    while True:
        try:
            with open(FULL_PATH, "r", encoding="utf-8") as f:
                content = f.read()

            if content.strip() and content != last_content:
                push_update(REPO_PATH, FILENAME)
                last_content = content
        except Exception as e:
            pass

        time.sleep(CHECK_DELAY)

if __name__ == "__main__":
    main()