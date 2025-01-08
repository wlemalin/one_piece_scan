import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def fetch_tweets(url='https://x.com/wsj_manga', output_file='infos_twitter.txt', max_tweets=30):
    """
    Récupère des tweets d'une page et les écrit dans un fichier uniquement s'ils contiennent "ONE PIECE".

    Args:
        url (str): L'URL de la page à scraper.
        output_file (str): Nom du fichier de sortie (par défaut 'infos_twitter.txt').
        max_tweets (int): Nombre maximal de tweets à récupérer (par défaut 30).
    """
    # Initialiser le navigateur
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        time.sleep(4)  # Temps pour charger la page

        # Ouvrir un fichier en mode écriture
        with open(output_file, 'w', encoding='utf-8') as file:
            tweets = driver.find_elements(By.XPATH, '//*[@data-testid="tweetText"]')
            count = 0

            for tweet in tweets:
                if count >= max_tweets:
                    break

                tweet_text = tweet.text
                if "ONE PIECE" in tweet_text:  # Vérifier si "ONE PIECE" est dans le contenu
                    file.write(f"Tweet {count + 1} :\n")
                    file.write(tweet_text + '\n')
                    file.write('-' * 50 + '\n')
                    count += 1

            if count == 0:
                file.write("No explanation for the delay were found.")
            print(f"{count} tweets contenant 'ONE PIECE' ont été enregistrés dans le fichier '{output_file}'.")

    except Exception as e:
        print("Erreur lors de la récupération des tweets :", e)

    finally:
        # Fermer le navigateur
        driver.quit()
