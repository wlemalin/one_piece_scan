#Suppression des redondances :Répétitions inutiles supprimées, cf reimportation des modules.
#Gestion centralisée des exceptions : Les exceptions liées à ReplicateError, FileNotFoundError, OSError, et ValueError sont gérées dans un seul bloc pour plus de lisibilité.
#Encodage explicite : Ajout d'encoding='utf-8' dans les ouvertures de fichier pour éviter les erreurs d'encodage potentielles.
#Amélioration des regex : Utilisation d'une f-string dans re.sub pour simplifier le remplacement.
#Validation des fichiers d'entrée : Gestion des erreurs potentielles lorsque le fichier d'entrée n'existe pas.

import os
import re
import time
from functools import wraps
import replicate
from replicate.exceptions import ReplicateError

response_file = "explanation.txt"

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
if not REPLICATE_API_TOKEN:
    raise EnvironmentError("REPLICATE_API_TOKEN is not set in the environment")

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
                    "meta/meta-llama-3-70b-instruct", input=input_data
                )
                return "".join(output)  # Joindre les parties de la réponse

            except (ReplicateError, FileNotFoundError, OSError, ValueError) as e:
                print(f"Erreur lors de l'envoi de la demande: {e}")
                time.sleep(10)
                return None

        return wrapper
    return decorator

@api_request_decorator(
    objective="Synthetise les infos sur la sortie du scan One Piece.",
    instructions=(
        '- **Synthesize the informations**'
        ' Below you will find the reasons why the last One Piece scan is not available.\n'
        ' Using these informations you will write a paragraph to explain the situation to one piece fans.\n'
        ' You will write a paragraph that clearly explains the reasons that caused the problem\n'
        ' If informations on the new release date are available, you should include it in your explanation.\n'
        ' Your answers should always contain close to 500 characters.'
    )
)
def synthesize_infos_with_llm(text: str) -> str | None:
    return text

@api_request_decorator(
    objective="Synthetise l'histoire",
    instructions=(
        '- **Synthesize the informations**'
        ' Below you will find a text of a video.\n'
        ' Using these informations you will write a paragraph to explain the situation.\n'
        ' You will write a paragraph that clearly summarizes the video.\n'
        ' Your answers should always contain close to 500 characters.'
    )
)
def synthesize_video_with_llm(text: str) -> str | None:
    return text

def replace_body_content(new_content: str, file_path: str = "explanation.html"):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        updated_content = re.sub(
            r'(<body.*?>)(.*?)(</body>)',
            fr'\1{new_content}\3',
            html_content,
            flags=re.DOTALL
        )

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        print("Contenu du body mis à jour avec succès.")

    except FileNotFoundError:
        print(f"Le fichier {file_path} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

def infos_cleanup(input_text: str = "infos_twitter.txt"):
    try:
        with open(input_text, 'r', encoding='utf-8') as infos:
            twitter_infos = infos.read()

        final_explanation = synthesize_infos_with_llm(twitter_infos)
        if final_explanation:
            replace_body_content(final_explanation)
            print("Réponse générée par Llama3 enregistrée avec succès:\n" + final_explanation)
        else:
            print("Aucune réponse reçue ou erreur lors de la récupération de la réponse.")

    except FileNotFoundError:
        print(f"Le fichier {input_text} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

if __name__ == "__main__":
    infos_cleanup()

