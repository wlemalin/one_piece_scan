from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_video_id(url):
    # Use regex to extract video ID from the given URL
    video_id = re.search(r'v=([a-zA-Z0-9_-]{11})', url)
    if video_id:
        return video_id.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

def get_subtitles(video_id, language='fr'):
    try:
        # Fetch the subtitles using YouTubeTranscriptApi
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])

        # Combine transcript into a single string
        subtitles = "\n".join([item['text'] for item in transcript])
        return subtitles
    except Exception as e:
        return str(e)

# Example usage
youtube_url = "https://www.youtube.com/watch?v=AZJm0uXFavM&ab_channel=MontCorvo"
video_id = get_video_id(youtube_url)
subtitles = get_subtitles(video_id)

if subtitles:
    print("Subtitles:\n")
    print(subtitles)
else:
    print("Subtitles not available.")
