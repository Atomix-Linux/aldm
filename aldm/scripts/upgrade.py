from check import check_update
from download_system import download_split_files
import sys

CHANNEL_FILE = "/zenkai_root/channel"

def read_channel():
    try:
        with open(CHANNEL_FILE, "r") as f:
            channel = f.read().strip()
        return channel
    except Exception as e:
        print(f"Cant read channel file: {e}")
        sys.exit(1)

def check_if_exists():
    channel = read_channel()
    if not check_update():
        print(f"System is up to date on channel '{channel}'. Aborting...")
        sys.exit(1)
    else:
        print(f"Downloading Latest system image for channel '{channel}'...")
        download_split_files(channel)

if __name__ == "__main__":
    check_if_exists()
