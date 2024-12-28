#Gestion des exceptions globales : Assurez-vous que le navigateur est fermé en cas d'erreur.
#Paramétrage explicite du driver : Ajout d'options pour Selenium afin d'améliorer les performances et éviter les messages inutiles.
#Réduction de l'utilisation de time.sleep : Remplacement par des attentes explicites (WebDriverWait) pour une meilleure gestion des chargements dynamiques.
#Limitation de la sortie console : Option pour enregistrer les tweets dans une liste ou un fichier.
#Flexibilité : Ajout de paramètres pour configurer le comportement (ex. : headless mode pour exécuter sans afficher le navigateur).

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def init_driver(headless=True):
    """Initialise et retourne le navigateur."""
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3")

    service = Service()  # Ajoutez le chemin du driver si nécessaire
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def open_twitter_profile(driver, username):
    """Accède à la page X (Twitter) du profil spécifié."""
    url = f'https://x.com/{username}'
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@data-testid="tweetText"]'))
        )
    except Exception as e:
        print(f"Erreur : La page du profil n'a pas pu être chargée. {e}")
        raise

def fetch_latest_tweets(driver, num_tweets=3):
    """Récupère et retourne le contenu des derniers tweets."""
    try:
        tweets = driver.find_elements(By.XPATH, '//*[@data-testid="tweetText"]')
        tweet_texts = [tweet.text for tweet in tweets[:num_tweets]]
        return tweet_texts
    except Exception as e:
        print("Erreur lors de la récupération des tweets :", e)
        return []

def close_driver(driver):
    """Ferme le navigateur."""
    driver.quit()

def latest_tweets(username, num_tweets=3, headless=True):
    """Récupère les derniers tweets d'un utilisateur donné."""
    driver = init_driver(headless)
    try:
        open_twitter_profile(driver, username)
        tweets = fetch_latest_tweets(driver, num_tweets)
        for i, tweet in enumerate(tweets, start=1):
            print(f"Tweet {i} :\n{tweet}\n{'-' * 50}")
        return tweets
    finally:
        close_driver(driver)

if __name__ == '__main__':
    latest_tweets('elonmusk', num_tweets=5, headless=False)
