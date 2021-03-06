import traceback
import json
import requests
import re

from urllib.parse import urlparse

from tasks.api_keys import KeyRing

API_KEY = KeyRing().get("phishtank")

URL = "https://checkurl.phishtank.com/checkurl/"
SCREENSHOTS_STORAGE_PATH = "/temp/phishtank"
SCREENSHOTS_SERVER_PATH = "static/phishtank"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"


def phishtank_check(url):
    try:
        if not API_KEY:
            print("No API key...!")
            return None

        response = {}

        headers = {
            "User-Agent": USER_AGENT,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        post_data = {"url": url, "format": "json", "app_key": API_KEY}

        response = requests.post(URL, post_data, headers=headers)
        if not response.status_code == 200:
            print("API key error!")
            return None
        else:
            response = json.loads(response.content)
            if "phish_id" in response["results"]:
                phish_id = response["results"]["phish_id"]

                try:
                    screenshot_path = phishtank_screenshot(phish_id)
                    if screenshot_path:
                        response["results"]["screenshot_path"] = screenshot_path
                except:
                    print("[PHISHTANK] Could not have a screenshot")

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


def phishtank_screenshot(phish_id):
    try:

        URL_main = f"https://www.phishtank.com/phish_screenshot.php?phish_id={phish_id}"

        regex_url = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

        if not API_KEY:
            print("No API key...!")
            return None

        response = {}

        headers = {"User-Agent": USER_AGENT}

        response = requests.get(URL_main, headers=headers)
        if not response.status_code == 200:
            print("API key error!")
            return None
        else:
            if response.content:
                content = response.content.decode("utf-8")
                matches = re.findall(regex_url, content)
                if matches:
                    screenshot_url = matches[0]
                    screenshot_name = urlparse(screenshot_url).path
                    r = requests.get(screenshot_url, allow_redirects=True)
                    with open(f"{SCREENSHOTS_STORAGE_PATH}{screenshot_name}", "wb") as f:
                        f.write(r.content)
                    return f"{SCREENSHOTS_SERVER_PATH}{screenshot_name}"

        return None

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None


def phishtank_tech_details(phish_id):
    try:

        URL_main = f"https://www.phishtank.com/phish_detail.php?phish_id={phish_id}"

        if not API_KEY:
            print("No API key...!")
            return None

        response = {}

        headers = {"User-Agent": USER_AGENT}

        response = requests.get(URL_main, headers=headers)
        if not response.status_code == 200:
            print("API key error!")
            return None
        else:
            response = response.content

        return response

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None  # parsing html to extract Verify and more
