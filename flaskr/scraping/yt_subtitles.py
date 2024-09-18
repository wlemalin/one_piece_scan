from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_video_id(url:str):
    """
    Function to get the video id using the giving link.
    arg:
        url: url of the video
    """
    video_id = re.search(r'v=([a-zA-Z0-9_-]{11})', url)
    if video_id:
        return video_id.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

def get_subtitles(video_id:str, language='fr'):
    """
    Function to get subtittles.
    args:
        video_id: id of the video
        language: a correct language (or list of languages).
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        subtitles = "\n".join([item['text'] for item in transcript])
        return subtitles
    
    except Exception as e:
        return str(e)




