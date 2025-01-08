import os
import re
import time
from functools import wraps

import replicate
from replicate.exceptions import ReplicateError

# Assurez-vous que la variable d'environnement est définie
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

if REPLICATE_API_TOKEN is None:
    raise EnvironmentError("REPLICATE_API_TOKEN is not set in the environment")
else:
    replicate.api_token = REPLICATE_API_TOKEN


def api_request_decorator(objective: str, instructions: str):
    def decorator(func):
        @wraps(func)
        def wrapper(text: str, *args, **kwargs):
            input_data = {
                'prompt': (
                    f"**Objective:** {objective}\n\n"
                    f"{instructions}\n\n"
                    f"**Original Prompt:**\n{text}"
                )
            }

            print(f"Infos envoyées à Llama3: {text}")

            try:
                output = replicate.run(
                    "meta/meta-llama-3-70b-instruct", input=input_data)
                explanations = "".join(output)  # Joindre les parties de la réponse
                return explanations

            except ReplicateError as e:
                print(f"Erreur liée à Replicate lors de l'envoi de la demande: {e}")
                time.sleep(10)
            except FileNotFoundError as e:
                print(f"Erreur : Le fichier spécifié n'a pas été trouvé: {e}")
                time.sleep(10)
            except OSError as e:
                print(f"Erreur système : {e}")
                time.sleep(10)
            except ValueError as e:
                print(f"Erreur de valeur : {e}")
                time.sleep(10)
            return None
        return wrapper
    return decorator


@api_request_decorator(
    objective="Synthetise les infos sur la sortie du scan One Piece.",
    instructions=(
        '- **Synthesize the informations**'
        ' Below you will find tweets that may contain the reasons why the last One Piece scan is not available.\n'
        ' Using theses informations you will write a paragraph to explain the situation to one piece fans.\n'
        ' You wil write a paragraph that clearly explains the reasons that caused the problem\n'
        ' If informations on the new release date is available, you should include it in your explanation.\n'
        ' You will only write the explanations in quote and do not write any introduction phrase before.\n'
        ' Your answers should always contain close to 500 characters.\n'
        'If the scan was released as expected just simply say so.\n'
        'If the text given to you does not provide an explanation, say that the reason of the delay is unknown.'
    )
)
def synthesize_infos_with_llm(text: str) -> str | None:
    """Envoie le texte à Llama3 via l'API Replicate pour synthétiser les infos Twitter."""
    return text


@api_request_decorator(
    objective="Synthetise l'histoire",
    instructions=(
        '- **Synthesize the informations**'
        ' Below you will find a subtitle from a video.\n'
        ' Using theses informations you will write a paragraph to explain the situation.\n'
        ' You will write a paragraph that clearly summarize the chapter to the fans with an hype intonation\n'
        ' Moreover, you will graduate the chapter on 10 in function of the sentiment of speecher in the video\n'
        ' Your answers should always contain close to 2000 characters.'
    )
)
def synthesize_video_with_llm(text: str) -> str | None:
    """
    Function to synthesize video by using replicate (llama3).

    Args:
        text: text to summarize
    """
    return text


def replace_body_content(new_content: str, file_path: str = "../templates/release_status.html"):
    try:
        # Lire le contenu du fichier HTML
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Expression régulière pour remplacer le contenu entre <p> et </p>
        updated_content = re.sub(
            r'(<p>)(.*?)(</p>)', rf'\1{new_content}\3', html_content, flags=re.DOTALL)

        # Écrire le contenu mis à jour dans le fichier HTML
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        print("Contenu entre <p> et </p> mis à jour avec succès.")

    except FileNotFoundError:
        print(f"Le fichier {file_path} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


def infos_cleanup(input_text="infos_twitter.txt"):
    """Synthesize informations about the delay and save the response"""
    with open(input_text) as infos:
        twitter_infos = infos.read()

    final_explanation = synthesize_infos_with_llm(twitter_infos)
    if final_explanation:
        replace_body_content(final_explanation)
        print(
            "Réponse généré par Llama3 enregistrée avec succès:\n" + final_explanation)
    else:
        print("Aucune réponse reçue ou erreur lors de la récupération de la réponse.")


if __name__ == "__main__":
    infos_cleanup()
