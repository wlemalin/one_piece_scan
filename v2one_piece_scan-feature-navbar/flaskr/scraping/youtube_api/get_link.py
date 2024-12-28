#Validation des paramètres d'entrée : Vérification que channel_id est une chaîne non vide.
#Gestion des erreurs : Ajout d'un message d'erreur si une clé essentielle est absente dans la réponse JSON.
#Refactorisation du format de sortie : Amélioration de la lisibilité du retour en cas d'erreur.
#Log des erreurs en mode développement (facultatif) : Ajout d'une variable DEBUG pour afficher plus de détails en cas d'erreurs.

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('YOUTUBE_API_KEY')
BASE_URL = 'https://www.googleapis.com/youtube/v3/search'
DEBUG = True  # Activer ou désactiver les logs pour le débogage


def get_video(channel_id: str, max_results: int = 7) -> list:
    """
    Function to fetch multiple last videos from a YouTube channel.
    
    Args:
        channel_id (str): The YouTube channel ID.
        max_results (int): Number of results to fetch.
        
    Returns:
        list: A list of dictionaries where each contains the video ID, 
              publish date, and channel name.
    """
    if not API_KEY:
        raise ValueError("API key not found. Please set the 'YOUTUBE_API_KEY' environment variable.")

    if not channel_id or not isinstance(channel_id, str):
        raise ValueError("Invalid channel ID. Please provide a valid YouTube channel ID as a string.")

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

        if 'items' not in data:
            return [{"error": "No items found in the response. Please check the channel ID or API quota."}]

        videos_info = []
        for item in data['items']:
            try:
                video_info = {
                    "video_id": item['id']['videoId'],
                    "date": item['snippet']['publishedAt'],
                    "name": item['snippet']['channelTitle']
                }
                videos_info.append(video_info)
            except KeyError as e:
                if DEBUG:
                    print(f"KeyError: {e}. Skipping invalid item: {item}")
                continue

        return videos_info

    except requests.exceptions.HTTPError as http_err:
        if DEBUG:
            print(f"HTTP error occurred: {http_err}")
        return [{"error": f"HTTP error occurred: {http_err}"}]
    except Exception as err:
        if DEBUG:
            print(f"Unexpected error occurred: {err}")
        return [{"error": f"An error occurred: {err}"}]


if __name__ == '__main__':
    CHANNEL_ID = 'UCu2e-o9q5_hZgPHCv8m1Qzg'
    videos = get_video(CHANNEL_ID, max_results=5)
    if videos:
        for video in videos:
            print(video)
