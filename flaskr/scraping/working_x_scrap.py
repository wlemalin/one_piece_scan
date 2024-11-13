import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def init_driver():
    """Initialise et retourne le navigateur."""
    return webdriver.Chrome()

def open_twitter_profile(driver, username):
    """Accède à la page X (Twitter) du profil spécifié."""
    url = f'https://x.com/{username}'
    driver.get(url)
    time.sleep(4)  # Attendre que la page se charge

def fetch_latest_tweets(driver, num_tweets=3):
    """Récupère et affiche le contenu des derniers tweets."""
    try:
        tweets = driver.find_elements(By.XPATH, '//*[@data-testid="tweetText"]')
        for i in range(min(num_tweets, len(tweets))):
            print(f"Tweet {i+1} :")
            print(tweets[i].text)
            print('-' * 50)
    except Exception as e:
        print("Erreur lors de la récupération des tweets:", e)

def close_driver(driver):
    """Ferme le navigateur."""
    driver.quit()

def latest_tweets(username):
    driver = init_driver()
    open_twitter_profile(driver, username)
    fetch_latest_tweets(driver)
    close_driver(driver)

# Appel de la fonction principale avec le nom d'utilisateur en argument
latest_tweets('elonmusk')
