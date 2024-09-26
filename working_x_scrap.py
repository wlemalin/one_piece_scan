from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Chemin vers le ChromeDriver (modifiez-le selon l'emplacement du driver sur votre machine)
driver_path = '/usr/bin/brave-browser'

# Initialiser le navigateur
driver = webdriver.Chrome()

# Accéder à la page X (Twitter) d'Elon Musk
url = 'https://x.com/elonmusk'
driver.get(url)

# Attendre quelques secondes pour permettre le chargement de la page
time.sleep(5)

# Récupérer le contenu du dernier post
try:
    # Localiser tous les éléments de tweets contenant le texte par leur attribut data-testid="tweetText"
    tweets = driver.find_elements(By.XPATH, '//*[@data-testid="tweetText"]')

    # Extraire et afficher le contenu des trois premiers tweets
    for i in range(min(3, len(tweets))):  # Récupérer jusqu'à 3 tweets
        print(f"Tweet {i+1} :")
        print(tweets[i].text)
        print('-' * 50)

except Exception as e:
    print("Erreur lors de la récupération des tweets:", e)

# Fermer le navigateur
driver.quit()
