import os
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


API_KEY = "AIzaSyC3eIU9dMEzqIGHyrFN6DTkQeXgjXrCfsY"

def get_video_rankings(api_key, keyword):
    youtube = build("youtube", "v3", developerKey=api_key)

    try:
        # Call the search.list method to get videos related to the keyword
        search_response = youtube.search().list(
            q=keyword,
            type="video",
            part="id,snippet",
            maxResults=10 
        ).execute()

        video_rankings = []

        # Extract video details from the search results
        for index, item in enumerate(search_response.get("items", [])):
            video_id = item["id"]["videoId"]
            video_title = item["snippet"]["title"]
            video_rankings.append({"rank": index + 1, "video_id": video_id, "title": video_title})

        return video_rankings

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return None

def main():
    print("Welcome to the YouTube Rank Tracker Tool!")

    # Input the keyword you want to track
    keyword = input("Enter the keyword to track: ")

    try:
        video_rankings = get_video_rankings(API_KEY, keyword)

        if video_rankings:
            # Display the rankings
            print("\nVideo Rankings:")
            for ranking in video_rankings:
                print(f"Rank: {ranking['rank']}, Video ID: {ranking['video_id']}, Title: {ranking['title']}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
