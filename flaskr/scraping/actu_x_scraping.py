import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def fetch_actus_tweets(url='https://x.com/OnePieceAnime', output_file='actus_twitter.txt', max_tweets=30):

    # Initialiser le navigateur
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        time.sleep(10)  # Temps pour charger la page

        # Ouvrir un fichier en mode écriture
        with open(output_file, 'w', encoding='utf-8') as file:
            tweets = driver.find_elements(By.XPATH, '//*[@data-testid="tweetText"]')
            count = 0

            for tweet in tweets:
                if count >= max_tweets:
                    break

                tweet_text = tweet.text
                file.write(f"Tweet {count + 1} :\n")
                file.write(tweet_text + '\n')
                file.write('-' * 50 + '\n')
                count += 1

            print(f"{count} tweets ont été enregistrés dans le fichier '{output_file}'.")

    except Exception as e:
        print("Erreur lors de la récupération des tweets :", e)

    finally:
        # Fermer le navigateur
        driver.quit()
