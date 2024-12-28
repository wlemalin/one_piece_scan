#Validation de l'URL YouTube : Ajout de support pour différents formats d'URL.
#Gestion des exceptions : Ajout de messages d'erreur détaillés pour différents types d'échecs.
#Typage explicite des fonctions : Pour une meilleure lisibilité et une utilisation facilitée.
#Ajout d'une fonction principale pour une exécution propre : Permet d'intégrer facilement ce script dans d'autres applications.

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import re

def get_video_id(url: str) -> str:
    """
    Extracts the video ID from a given YouTube URL.

    Args:
        url (str): The URL of the YouTube video.

    Returns:
        str: The video ID.

    Raises:
        ValueError: If the URL is invalid or doesn't contain a video ID.
    """
    video_id = re.search(r'(?:v=|youtu\.be/|embed/)([a-zA-Z0-9_-]{11})', url)
    if video_id:
        return video_id.group(1)
    else:
        raise ValueError("Invalid YouTube URL. Please provide a valid video link.")

def get_subtitles(video_id: str, language: str = 'fr') -> str:
    """
    Fetches subtitles for a given YouTube video in the specified language.

    Args:
        video_id (str): The ID of the YouTube video.
        language (str): The desired language for subtitles.

    Returns:
        str: Subtitles as a single string.

    Raises:
        Exception: If subtitles cannot be retrieved due to various reasons.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        subtitles = "\n".join([item['text'] for item in transcript])
        return subtitles
    except TranscriptsDisabled:
        return "Subtitles are disabled for this video."
    except NoTranscriptFound:
        return f"No subtitles found for the video in '{language}' language."
    except Exception as e:
        return f"An error occurred while fetching subtitles: {e}"

if __name__ == '__main__':
    # Exemple d'utilisation
    try:
        url = input("Enter the YouTube video URL: ")
        video_id = get_video_id(url)
        print(f"Video ID: {video_id}")
        
        subtitles = get_subtitles(video_id, language='fr')
        print("\nSubtitles:\n", subtitles)
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")





