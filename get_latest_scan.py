import os
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Création d'un DataFrame pour les sites et leurs URL
sites_data = {'website': ['lelmanga', 'onepiecescan'],
              'url': ['https://www.lelmanga.com/category/one-piece', 'https://onepiecescan.fr']}

df_sites = pd.DataFrame(sites_data)

# Compteur global pour suivre le nombre d'appels de la fonction get_latest_chapter
SCRAP_COUNT = 0
NEW_SCAN = ""


def get_latest_chapter(url: str) -> str | None:
    """
    Scrape the latest chapter from the URL corresponding to the global counter.

    Returns:
        str: The latest chapter found, or None if none found.
    """

    global SCRAP_COUNT

    # allows to iterate over websites if needed
    current_site = df_sites.iloc[SCRAP_COUNT]
    url = current_site['url']
    site_name = current_site['website']

    SCRAP_COUNT += 1  # Incrémenter le compteur après chaque appel


    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        if site_name == 'lelmanga':
            chapitres = soup.find_all('div', class_='epxs')
        elif site_name == 'onepiecescan':
            # Utilisation de la div avec l'ID 'All_chapters' pour récupérer les chapitres
            chapitres_container = soup.find('div', id='All_chapters')
            if chapitres_container:
                chapitres = chapitres_container.find_all('a')
            else:
                chapitres = []
        else:
            print(f"Site {site_name} non pris en charge.")
            return None

        new_latest = None
        if chapitres:
            new_latest = ''.join(re.findall(r'\d+', chapitres[0].text.strip()))
            return new_latest

    else:
        print(f"Échec de la requête : {response.status_code}")

    return None


def is_scan_delayed(new_chap: str | None, file_name: str = "last_scan_available.txt") -> bool:
    """
    Compare le dernier scan récupéré avec le fichier local et met à jour si nécessaire.

    Args:
        new_chap (str | None): Le dernier scan récupéré.
        file_name (str): Nom du fichier stockant le dernier scan.

    Returns:
        bool: True si le scan est déjà enregistré, False sinon.
    """
    global NEW_SCAN

    
    if new_chap and not os.path.exists(file_name):
        with open(file_name, 'w') as file:
            file.write(new_chap)
            NEW_SCAN = new_chap
        return True
    elif new_chap:
        with open(file_name, 'r') as file:
            current_latest = file.read().strip()

        if current_latest == new_chap:
            return False
        else:
            with open(file_name, 'w') as file:
                file.write(new_chap)
                NEW_SCAN = new_chap
            return True
    else:
        return False


if __name__ == '__main__':
    # load_urls()
    # Boucle pour exécuter plusieurs fois et changer le site à chaque appel
    for i in df_sites['url']:  # Remplace 5 par le nombre d'appels souhaité
        scraped_scan = get_latest_chapter(i)
        is_scan_delayed(scraped_scan)
        if NEW_SCAN != "" or SCRAP_COUNT == len(df_sites):
            break
    if NEW_SCAN != "":
        print(f"Nouveau chapitre {NEW_SCAN} enregistré.")
    else:
        print("No new chapter found.")
        # TWEETER LOOKUP
