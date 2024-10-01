import re
import requests
from bs4 import BeautifulSoup

def fetch_decorator(func):
    """
    Decorator function that fetches the content from a URL and 
    parses it using the provided parsing function.
    """
    def wrapper(url: str):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return func(soup)
        else:
            print(f"Échec de la requête pour {url}: {response.status_code}")
            return None
    return wrapper

@fetch_decorator
def parse_lelmanga(soup: BeautifulSoup):
    """
    Function to parse the latest chapter number from the LelManga website.
    
    Args:
        url (str): The URL of the page from which the content is retrieved.

    Returns:
        str: The latest chapter number extracted from the HTML content.
    """
    last_chapitre = soup.find_all('div', class_='epxs')[0].get_text(strip=True)
    return re.findall(r'\d+', last_chapitre)[0]

@fetch_decorator
def parse_onepiecescan(soup: BeautifulSoup):
    """
    Function to parse the latest chapter number from the OnePieceScan website.
    
    Args:
        url (str): The URL of the page from which the content is retrieved.

    Returns:
        str: The latest chapter number extracted from the HTML content.
    """
    last_chapitre = soup.find_all('a', href=True, string=re.compile(r'One Piece Scan Chapitre (\d+)'))[0].get_text(strip=True)
    return re.findall(r'\d+', last_chapitre)[0]

@fetch_decorator
def parse_lelscans(soup: BeautifulSoup):
    """
    Function to parse the latest chapter number from the LelScans website.
    
    Args:
        url (str): The URL of the page from which the content is retrieved.

    Returns:
        str: The latest chapter number extracted from the HTML content.
    """
    last_chapitre = soup.find_all('option', value=True, string=re.compile(r'(\d+)'))[0].get_text()
    return re.findall(r'\d+', last_chapitre)[0]

@fetch_decorator
def parse_dexerto(soup: BeautifulSoup):
    """
    Function to parse all paragraph texts from the Dexerto website.
    
    Args:
        url (str): The URL of the page from which the content is retrieved.

    Returns:
        str: A single string concatenating all paragraph texts from the HTML content.
    """
    content = [text.get_text() for text in soup.find_all('p')]
    return ' '.join(content)

@fetch_decorator
def parse_dexerto_anime_page(soup: BeautifulSoup):
    """
    Function to parse articles containing One Piece chapter information 
    from the Dexerto anime page.
    
    Args:
        url (str): The URL of the page from which the content is retrieved.

    Returns:
        list: A list of dictionaries, each containing the title, 
              scan number, and URL of an article.
    """
    pattern = r'One\s*Piece\s*Chapitre\s*(\d+)\s*:\s*date\s*de\s*sortie'
    articles = []
    for item in soup.find_all('a', href=True, string=re.compile(pattern, re.IGNORECASE)):
        article = {
            'title': item.get_text(),
            'scan': int(re.findall(r'\d+', item.get_text())[0]),
            'url': item['href']
        }
        articles.append(article)
    return articles
        
def parse_dexerto_anime(max_pages: int = 3):
    """
    Function to parse articles from multiple pages of the Dexerto anime section.
    
    Args:
        max_pages (int): The maximum number of pages to parse (default is 3).

    Returns:
        list: A list of all articles parsed from the specified number of pages.
    """
    articles = []
    for page in range(max_pages):
        articles.extend(parse_dexerto_anime_page(f'https://www.dexerto.fr/anime/page/{page+1}/'))
    return articles



if __name__ == '__main__':
    # print(parse_lelmanga('https://www.lelmanga.com/category/one-piece'))
    # print(parse_onepiecescan('https://onepiecescan.fr'))
    # print(parse_lelscans('https://lelscans.net/lecture-en-ligne-one-piece'))
    tester = parse_dexerto_anime()[0]
    print(type(tester['url']))
    print(type(tester['title']))
    print(type(tester['scan']))
    # print(parse_dexerto('https://www.dexerto.fr/anime/one-piece-chapitre-1128-informations-1588109/'))

