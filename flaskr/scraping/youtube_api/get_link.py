import os
import html
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv('YOUTUBE_API_KEY')
BASE_URL = 'https://www.googleapis.com/youtube/v3/search'


def get_video(channel_id: str, max_results: int = 7) -> list:
    """
    Function to fetch multiple lasts videos from a YouTube channel.
    
    Args:
        channel_id (str): The YouTube channel ID.
        max_results (int): Number of results to fetch.
        
    Returns:
        list: A list of dictionaries where each contains the video ID, 
            publish date, and channel name.

            Example:
            [
                {
                    "video_id": "000000000",
                    "date": "2024-09-15T08:00:18Z",
                    "name": "Channel"
                },
                {
                    "video_id": "000000001",
                    "date": "2024-09-08T08:00:37Z",
                    "name": "Cannel"
                }
            ]
    """
    if not API_KEY:
        raise ValueError("API key not found. Please set the 'YOUTUBE_API_KEY' environment variable.")

    params = {
        'key': API_KEY,
        'channelId': channel_id,
        'part': 'snippet',
        'order': 'date',
        'maxResults': max_results
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if 'items' not in data or not data['items']:
            return []

        videos_info = []
        for item in data['items']:
            video_info = {
                "video_id": item['id']['videoId'],
                "date": item['snippet']['publishedAt'],
                "name": item['snippet']['channelTitle'],
                "title": html.unescape(item['snippet']['title'])
            }
            videos_info.append(video_info)

        return videos_info

    except requests.exceptions.HTTPError as http_err:
        return [{"error": f"HTTP error occurred: {http_err}"}]
    except Exception as err:
        return [{"error": f"An error occurred: {err}"}]


if __name__ == '__main__':
    CHANNEL_ID = 'UCu2e-o9q5_hZgPHCv8m1Qzg'
    # get_video(CHANNEL_ID)
