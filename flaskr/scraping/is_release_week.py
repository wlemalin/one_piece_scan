import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

from get_latest_scan import *
from x_scraping import fetch_tweets

# Ajouter la racine du projet au chemin Python
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from flaskr.generate.llm_summary import infos_cleanup

def process_scan_release(file_path):
    """
    Process the scan release information from a given CSV file
    and display relevant information about the current and next release.

    Parameters:
        file_path (str): Path to the CSV file containing release data.
    """
    # Load the data from the CSV file
    df = pd.read_csv(file_path)

    # Get the current week
    current_week = datetime.now().isocalendar()[1]

    # Find the row corresponding to the current week
    current_week_row = df[df['Week'].str.contains(f'Week {current_week:02}')]

    if not current_week_row.empty:
        # Extract information about the current week
        # First row, expected to be unique
        current_info = current_week_row.iloc[0]
        chapter = current_info['Chapter']

        if chapter.isdigit():
            # Chapter is numeric, meaning a release is expected
            print(
                f"{current_info['Week']} : Expected release of scan {chapter}.")
            return chapter
        else:
            # No scan release this week; find the next release
            next_release = df[df['Chapter'].apply(lambda x: str(x).isdigit()) & (
                df.index > current_week_row.index[0])].head(1)

            if not next_release.empty:
                next_info = next_release.iloc[0]
                print(
                    f"{current_info['Week']} : No scan release this week ({chapter}).")
                print(
                    f"Next scan : {next_info['Week']} scan {next_info['Chapter']} expected on {next_info['Oficial WSJ Release Date']}.")
            else:
                print("Aucune prochaine sortie de scan trouvée dans le tableau.")
            return None
    else:
        # Current week is not in the table
        print("La semaine actuelle ne figure pas dans le tableau.")
        return None


expected_release = process_scan_release("release_date.csv")
print(expected_release)
lelmanga = parse_lelmanga('https://www.lelmanga.com/category/one-piece')
opscan = parse_onepiecescan('https://onepiecescan.fr')
lelscans = parse_lelscans('https://lelscans.net/lecture-en-ligne-one-piece')
latest_scan = sorted([lelmanga, opscan, lelscans])[0]
print(latest_scan)


if expected_release == None:
    with open("infos_twitter.txt", "w", encoding="utf-8") as file:
        file.write(
            "According to the official schedule, there is no scan release expected this week.")

elif expected_release == latest_scan:
    with open("infos_twitter.txt", "w", encoding="utf-8") as file:
        file.write(
            f"As expected from the official schedule, the scan {latest_scan} was released this week.")

else:
    fetch_tweets()

infos_cleanup()
