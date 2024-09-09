import os
from icecream import ic
import requests
from bs4 import BeautifulSoup


def get_latest_chapter(url: str = "https://www.lelmanga.com/category/one-piece") -> str | None:
    """
    Scrape the latest chapter from the given URL and compare it to the saved chapter.

    Args:
        url (str): URL of the website to scrape.
        file_name (str): Path to the file that stores the last scanned chapter.

    Returns:
        bool: True if a new chapter is found, False otherwise.
    """

    response = requests.get(url)

    if response.status_code == 200:

        soup = BeautifulSoup(response.content, 'html.parser')

        chapitres = soup.find_all('div', class_='epxs')

        new_latest = None
        if chapitres:
            new_latest = chapitres[0].text.strip()
            return new_latest

    print(f"Échec de la requête : {response.status_code}")
    return None


def is_scan_delayed(new_chap: str | None, file_name: str = "last_scan_available.txt") -> bool:
    if new_chap and os.path.exists(file_name) == False:
        with open(file_name, 'w') as file:
            file.write(new_chap)
            print(
                f"Fichier créé et chapitre {new_chap} enregistré.")
            return False
    elif new_chap:
        with open(file_name, 'r') as file:
            current_latest = file.read().strip()

        if current_latest == new_chap:
            print(
                f"Le chapitre {current_latest} est déjà enregistré.")
            return True
        else:
            with open(file_name, 'w') as file:
                file.write(new_chap)
            print(
                f"Nouveau chapitre {new_chap} enregistré.")
            return False
    else:
        print("Aucun chapitre trouvé.")
        return False

if __name__=='__main__':
    scraped_scan = get_latest_chapter()
    ic(is_scan_delayed(scraped_scan))
