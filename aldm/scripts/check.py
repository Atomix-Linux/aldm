import os
import requests
import sys

DEPLOYS_DIR = "/zenkai_root/deploys"
CHANNEL_FILE = "/zenkai_root/channel"
GITHUB_API = "https://api.github.com/repos/Atomix-Linux/atomix/releases"

def get_channel():
    try:
        with open(CHANNEL_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("❌ Channel file not found:", CHANNEL_FILE)
        sys.exit(1)

def get_current_version():
    try:
        deploy_dirs = [d for d in os.listdir(DEPLOYS_DIR) if d.startswith("atomix-")]
        if not deploy_dirs:
            raise FileNotFoundError("No deployment found in /zenkai_root/deploys")

        deploy_dirs.sort(reverse=True)
        latest_deploy = deploy_dirs[0]  # e.g. atomix-v2025.07.01_f73e395

        # Format: atomix-<version>_<tag>
        without_prefix = latest_deploy[len("atomix-"):]
        version, tag_or_commit = without_prefix.split("_", 1)

        return version.strip(), tag_or_commit.strip()

    except Exception as e:
        print(f"❌ Error reading current version: {e}")
        sys.exit(1)


def parse_version_tag(tag):
    # Jeśli tag ma format "1_f73e395" lub "v2025.07.15_f73e395"
    if "_" in tag:
        version, commit = tag.split("_", 1)
    else:
        version, commit = tag, ""
    return version, commit

def get_latest_version(channel="stable"):
    response = requests.get(GITHUB_API)
    response.raise_for_status()
    releases = response.json()

    for release in releases:
        if channel == "stable" and not release["draft"] and not release["prerelease"]:
            return parse_version_tag(release["tag_name"])
        elif channel == "unstable" and not release["draft"] and release["prerelease"]:
            return parse_version_tag(release["tag_name"])

    raise Exception("❌ No release found for the selected channel.")


def check_update():
    channel = get_channel()
    local_version, local_commit = get_current_version()

    print(f"🔎 Checking for updates on '{channel}' channel...")
    print(f"💻 Installed version: {local_version} ({local_commit})")

    latest_version, latest_commit = get_latest_version(channel)

    print(f"📦 Latest available: {latest_version} ({latest_commit})")

    if local_version != latest_version or local_commit != latest_commit:
        print("⬆️  Update available!")
        return True
    else:
        print("✅ System is up to date.")
        return False



if __name__ == "__main__":
    check_update()
