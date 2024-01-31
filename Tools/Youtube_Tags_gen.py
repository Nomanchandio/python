import random
from googleapiclient.discovery import build

API_KEY = "AIzaSyC3eIU9dMEzqIGHyrFN6DTkQeXgjXrCfsY"

def get_youtube_tags(keyword):
    youtube = build("youtube", "v3", developerKey=API_KEY)

    # Call the search.list method to search for videos related to the keyword
    search_response = youtube.search().list(
        q=keyword,
        type="video",
        part="id",
        maxResults=5
    ).execute()

    video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]

    tags = []
    for video_id in video_ids:
        # Call the videos.list method to get video details, including tags
        video_response = youtube.videos().list(
            id=video_id,
            part="snippet"
        ).execute()

        # Check if the "tags" key exists in the response
        if "tags" in video_response["items"][0]["snippet"]:
            video_tags = video_response["items"][0]["snippet"]["tags"]
            tags.extend(video_tags)

    return tags

def main():
    print("Welcome to the YouTube Tag Generator Tool!")

    keyword = input("Enter the keyword to generate tags: ")

    generated_tags = get_youtube_tags(keyword)

    print("\nGenerated YouTube Tags:")
    for tag in generated_tags:
        print(tag)

if __name__ == "__main__":
    main()
