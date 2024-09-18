import os
import re
from typing import List, Optional, Tuple
import requests
from bs4 import BeautifulSoup


def get_latest_chapter(urls: List[str]) -> Tuple[Optional[str], Optional[str]]:
    """
    Scrape the latest chapter from the given list of URLs.
    Args:
        urls (List[str]): List of URLs to scrape.
    Returns:
        Tuple[Optional[int], Optional[str]]: The highest chapter number and the website it was found on,
                                             or (None, None) if no chapters were found.
    """
    highest_chapter = None
    highest_chapter_site = None

    for url in urls:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            chapitres = None

            # Determine the site based on the URL
            if 'lelmanga.com' in url:
                chapitres = soup.find_all('div', class_='epxs')
                site_name = 'lelmanga'

            elif 'onepiecescan' in url:
                # Utilisation de la div avec l'ID 'All_chapters' pour récupérer les chapitres
                chapitres_container = soup.find('div', id='All_chapters')
                if chapitres_container:
                    chapitres = chapitres_container.find_all('a')
                else:
                    chapitres = []
                site_name = 'onepiecescan'

            if chapitres:  # clean the string, keep the numbers
                chapter_text = chapitres[0].text.strip()
                chapter_number = ''.join(re.findall(r'\d+', chapter_text))
                chapter_number = int(chapter_number)
                if chapter_number:
                    if highest_chapter is None or chapter_number > highest_chapter:
                        highest_chapter = chapter_number
                        highest_chapter_site = site_name
        else:
            print(f"Échec de la requête pour {url}: {response.status_code}")

    highest_chapter = str(highest_chapter)
    return highest_chapter, highest_chapter_site


def is_scan_delayed(fetched_chap: str | None, file_name: str = "last_scan_available.txt") -> bool:
    """
    Compare le dernier scan récupéré avec le fichier local et met à jour si nécessaire.

    Args:
        new_chap (str | None): Le dernier scan récupéré.
        file_name (str): Nom du fichier stockant le dernier scan.

    Returns:
        bool: True si le scan est déjà enregistré, False sinon.
    """
    if fetched_chap:
        with open(file_name, 'r') as file:
            current_latest = file.read().strip()

        if current_latest == fetched_chap:
            return True
        else:
            with open(file_name, 'w') as file:
                file.write(fetched_chap)
            return False
    else:
        return False


def create_last_scan_file(file_name: str = "last_scan_available.txt"):
    if not os.path.exists(file_name):
        with open(file_name, 'w'):
            pass


# Example usage
if __name__ == '__main__':
    urls = [
        'https://www.lelmanga.com/category/one-piece',
        'https://onepiecescan.fr',
    ]
    create_last_scan_file()
    latest_chapter, source_site = get_latest_chapter(urls)
    is_delayed = is_scan_delayed(latest_chapter)
    if is_delayed:
        print(
            f"Le chapitre trouvé le plus récent est encore le  n°{latest_chapter}. pourquoi?")
    else:
        print(
            f"Nouveau scan n°{latest_chapter} enregistré depuis {source_site}.")
