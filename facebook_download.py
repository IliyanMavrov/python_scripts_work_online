#!/usr/bin/python3

import requests

import re

import os


def download_private_facebook_video(url, email, password, output_path="downloads"):

    """

    Download a private Facebook video using your credentials.

    :param url: Facebook video URL
    :param email: Your Facebook email
    :param password: Your Facebook password
    :param output_path: Path to save the downloaded video
    """

    # Facebook login URL
    login_url = "https://www.facebook.com/login.php"

    # Start a session to maintain cookies
    session = requests.Session()

    try:
        print("Logging in to Facebook...")

        # Get the login page to retrieve necessary cookies and tokens
        login_page = session.get(login_url)

        if login_page.status_code != 200:
            print("Failed to fetch the Facebook login page.")
            return

        # Extract the lsd token for the login request
        lsd_token = re.search(r'name="lsd" value="(.*?)"', login_page.text)
        if not lsd_token:
            print("Failed to retrieve authentication token.")
            return

        lsd_token = lsd_token.group(1)

        # Prepare login payload
        payload = {
            "email": email,
            "pass": password,
            "lsd": lsd_token,
        }

        # Post login request
        response = session.post(login_url, data=payload)

        if "c_user" not in session.cookies:
            print("Login failed. Please check your credentials.")
            return

        print("Login successful!")

        # Fetch the video page
        print("Fetching video page...")
        video_page = session.get(url)

        if video_page.status_code != 200:
            print("Failed to fetch the video page.")
            return

        # Extract the video URL from the page source
        video_url = re.search(r'"playable_url":"(https:[^"]+)"', video_page.text)
        if not video_url:
            print("Failed to extract video URL. The video might not be accessible.")
            return

        # Decode and clean the video URL
        video_url = video_url.group(1).replace("\\u0025", "%").replace("\\", "")

        print(f"Video URL extracted: {video_url}")

        # Download the video file

        print("Downloading video...")

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        video_data = session.get(video_url, stream=True)
        file_name = os.path.join(output_path, "facebook_private_video.mp4")

        with open(file_name, "wb") as file:
            for chunk in video_data.iter_content(chunk_size=1024):
                file.write(chunk)

        print(f"Video downloaded successfully! Saved as: {file_name}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        session.close()


if __name__ == "__main__":

    # Input your Facebook credentials and the video URL
    fb_email = input("Enter your Facebook email: ")
    fb_password = input("Enter your Facebook password: ")
    video_url = input("Enter the Facebook video URL: ")

    download_private_facebook_video(video_url, fb_email, fb_password)
    