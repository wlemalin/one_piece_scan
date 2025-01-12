import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def fetch_actus_tweets(url='https://x.com/OnePieceAnime', max_tweets=30):
    # Initialiser le navigateur
    driver = webdriver.Chrome()
    text_output = ""

    try:
        driver.get(url)
        time.sleep(10)  # Temps pour charger la page

        tweets = driver.find_elements(By.XPATH, '//*[@data-testid="tweetText"]')
        count = 0

        for tweet in tweets:
            if count >= max_tweets:
                break

            tweet_text = tweet.text
            text_output += f"Tweet {count + 1} :\n"
            text_output += tweet_text + '\n'
            text_output += '-' * 50 + '\n'
            count += 1

        print(f"{count} tweets ont été récupérés.")

    except Exception as e:
        print("Erreur lors de la récupération des tweets :", e)

    finally:
        # Fermer le navigateur
        driver.quit()

    return text_output
