#Gestion des exceptions : Ajout de la gestion des erreurs pour éviter que le programme ne plante en cas de problèmes avec les requêtes ou le parsing.
#Validation des données : Vérification que les éléments retournés par soup.find_all ne sont pas vides avant de tenter d'extraire des données.
#Refactorisation : Éviter les répétitions de code dans le décorateur et simplifier certaines fonctions pour améliorer la lisibilité.
#Typage des fonctions : Ajout explicite des annotations de type pour clarifier les retours.

import re
import requests
from bs4 import BeautifulSoup
from typing import Callable, List, Dict, Optional, Union

def fetch_decorator(func: Callable[[BeautifulSoup], Union[str, List, Dict]]) -> Callable[[str], Optional[Union[str, List, Dict]]]:
    """
    Decorator function that fetches the content from a URL and 
    parses it using the provided parsing function.
    """
    def wrapper(url: str) -> Optional[Union[str, List, Dict]]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            return func(soup)
        except requests.exceptions.RequestException as e:
            print(f"Échec de la requête pour {url}: {e}")
        except Exception as e:
            print(f"Erreur inattendue lors du parsing de {url}: {e}")
        return None
    return wrapper

@fetch_decorator
def parse_lelmanga(soup: BeautifulSoup) -> Optional[str]:
    """
    Parse the latest chapter number from the LelManga website.
    """
    chapters = soup.find_all('div', class_='epxs')
    if chapters:
        last_chapitre = chapters[0].get_text(strip=True)
        return re.findall(r'\\d+', last_chapitre)[0]
    return None

@fetch_decorator
def parse_onepiecescan(soup: BeautifulSoup) -> Optional[str]:
    """
    Parse the latest chapter number from the OnePieceScan website.
    """
    links = soup.find_all('a', href=True, string=re.compile(r'One Piece Scan Chapitre (\\d+)'))
    if links:
        last_chapitre = links[0].get_text(strip=True)
        return re.findall(r'\\d+', last_chapitre)[0]
    return None

@fetch_decorator
def parse_lelscans(soup: BeautifulSoup) -> Optional[str]:
    """
    Parse the latest chapter number from the LelScans website.
    """
    options = soup.find_all('option', value=True, string=re.compile(r'(\\d+)'))
    if options:
        last_chapitre = options[0].get_text()
        return re.findall(r'\\d+', last_chapitre)[0]
    return None

@fetch_decorator
def parse_dexerto(soup: BeautifulSoup) -> Optional[str]:
    """
    Parse all paragraph texts from the Dexerto website.
    """
    paragraphs = soup.find_all('p')
    if paragraphs:
        content = [text.get_text() for text in paragraphs]
        return ' '.join(content)
    return None

@fetch_decorator
def parse_dexerto_anime_page(soup: BeautifulSoup) -> Optional[List[Dict[str, Union[str, int]]]]:
    """
    Parse articles containing One Piece chapter information from the Dexerto anime page.
    """
    pattern = r'One\\s*Piece\\s*Chapitre\\s*(\\d+)\\s*:\\s*date\\s*de\\s*sortie'
    articles = []
    links = soup.find_all('a', href=True, string=re.compile(pattern, re.IGNORECASE))
    for item in links:
        try:
            articles.append({
                'title': item.get_text(),
                'scan': int(re.findall(r'\\d+', item.get_text())[0]),
                'url': item['href']
            })
        except (IndexError, ValueError):
            print(f"Impossible d'extraire les informations de l'article: {item}")
            continue
    return articles if articles else None

def parse_dexerto_anime(max_pages: int = 3) -> List[Dict[str, Union[str, int]]]:
    """
    Parse articles from multiple pages of the Dexerto anime section.
    """
    articles = []
    for page in range(1, max_pages + 1):
        url = f'https://www.dexerto.fr/anime/page/{page}/'
        page_articles = parse_dexerto_anime_page(url)
        if page_articles:
            articles.extend(page_articles)
    return articles


if __name__ == '__main__':
    results = parse_dexerto_anime(max_pages=2)
    if results:
        for article in results:
            print(f"Title: {article['title']}, Scan: {article['scan']}, URL: {article['url']}")
