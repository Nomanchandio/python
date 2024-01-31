import os
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

API_KEY = "AIzaSyC3eIU9dMEzqIGHyrFN6DTkQeXgjXrCfsY"

def extract_video_tags(api_key, video_id):
    youtube = build("youtube", "v3", developerKey=api_key)

    try:
        # Call the videos.list method to get details of the specified video
        video_response = youtube.videos().list(
            part="snippet",
            id=video_id
        ).execute()

        # Extract video details including tags
        video_details = video_response.get("items", [])[0]
        video_title = video_details["snippet"]["title"]
        video_tags = video_details["snippet"].get("tags", [])

        return video_title, video_tags

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return None, None

def main():
    print("Welcome to the YouTube Tag Extractor Tool!")

  
    video_url = input("Enter the YouTube video URL: ")

    try:
        # Extract video ID from the URL
        video_id = None

        if "youtu.be" in video_url:
            video_id = video_url.split("/")[-1].split("?")[0]
        elif "youtube.com" in video_url:
            video_id = video_url.split("v=")[-1].split("&")[0]

        if video_id:
            video_title, video_tags = extract_video_tags(API_KEY, video_id)

            if video_title and video_tags:
                # Display video details and tags
                print(f"\nVideo Title: {video_title}")
                print("Video Tags:")
                for tag in video_tags:
                    print(f"- {tag}")
        else:
            print("Invalid YouTube video URL. Please provide a valid URL.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
