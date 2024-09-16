import os
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv('YOUTUBE_API_KEY')
BASE_URL = 'https://www.googleapis.com/youtube/v3/search'


def get_last_video(channel_id: str, max_results: int = 1) -> str:
    """
    Function to fetch the URL of the latest video from a YouTube channel.
    
    Args:
        channel_id (str): The YouTube channel ID.
        max_results (int): Number of results to fetch (default is 1).
        
    Returns:
        str: The URL of the latest video or an error message.
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
            return "No videos found for this channel."

        video_id = data['items'][0]['id']['videoId']
        return video_id

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"An error occurred: {err}"


if __name__ == '__main__':
    CHANNEL_ID = 'UCu2e-o9q5_hZgPHCv8m1Qzg'
    print(get_last_video(CHANNEL_ID))
