import os
import re
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs


API_KEY = "AIzaSyC3eIU9dMEzqIGHyrFN6DTkQeXgjXrCfsY"

def get_channel_id(api_key, channel_input):
    youtube = build("youtube", "v3", developerKey=api_key)

    # Check if the input is a full channel URL
    parsed_url = urlparse(channel_input)
    if parsed_url.netloc == "www.youtube.com" and parsed_url.path == "/channel":
        query_params = parse_qs(parsed_url.query)
        return query_params.get("channel_id", [None])[0]

    # If it's not a full channel URL, assume it's a channel name
    # Call the search.list method to get information about the specified channel
    search_response = youtube.search().list(
        q=channel_input,
        type="channel",
        part="id"
    ).execute()

    # Extract the channel ID from the search results
    channel_id = search_response.get("items", [])[0]["id"]["channelId"] if search_response.get("items") else None

    return channel_id

def get_channel_info(api_key, channel_id):
    youtube = build("youtube", "v3", developerKey=api_key)

    # Call the channels.list method to get information about the specified channel
    channel_response = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    ).execute()

    # Extract relevant information from the response
    channel_data = channel_response.get("items", [])[0]["snippet"]
    channel_stats = channel_response.get("items", [])[0]["statistics"]

    return {
        "channel_title": channel_data.get("title"),
        "channel_description": channel_data.get("description"),
        "published_at": channel_data.get("publishedAt"),
        "subscriber_count": channel_stats.get("subscriberCount"),
        "view_count": channel_stats.get("viewCount"),
        "video_count": channel_stats.get("videoCount"),
    }

def main():
    print("Welcome to the YouTube Channel Audit Tool!")

    # Input the YouTube channel name or URL
    channel_input = input("Enter the YouTube Channel name or URL: ")

    # Extract the channel ID
    channel_id = get_channel_id(API_KEY, channel_input)

    if not channel_id:
        print("Unable to determine the channel ID. Please check your input.")
        return

    channel_info = get_channel_info(API_KEY, channel_id)

    # Display channel information
    print("\nChannel Information:")
    print(f"Title: {channel_info['channel_title']}")
    print(f"Description: {channel_info['channel_description']}")
    print(f"Published At: {channel_info['published_at']}")
    print(f"Subscriber Count: {channel_info['subscriber_count']}")
    print(f"Total Views: {channel_info['view_count']}")
    print(f"Total Videos: {channel_info['video_count']}")

if __name__ == "__main__":
    main()
