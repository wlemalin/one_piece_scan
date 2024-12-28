#ajout gestionnaire de contexte (with sqlite3.connect) pour une meilleure gestion des connexions.
#ajout messages d'erreur détaillés pour faciliter le débogage.
#division des fonctions
#opti des imports
#ajout notations
#Suppression des répétitions

import sqlite3
import os
from generate.llm_summary import synthesize_video_with_llm, synthesize_infos_with_llm
from scraping.yt_subtitles import get_subtitles
from scraping.youtube_api.get_link import get_video
from scraping.get_latest_scan import parse_dexerto_anime, parse_dexerto


# Configurations
DATABASE = os.path.join('instance', 'flaskr.sqlite')


def get_connection():
    """Get a database connection."""
    if not os.path.exists(DATABASE):
        raise FileNotFoundError(f"Database not found at {DATABASE}")
    return sqlite3.connect(DATABASE)


def entry_exists(conn: sqlite3.Connection, table: str, **conditions) -> bool:
    """
    Check if an entry exists in a given table with specific conditions.

    Args:
        conn (sqlite3.Connection): Database connection.
        table (str): Table name.
        conditions: Column-value pairs to check.

    Returns:
        bool: True if the entry exists, False otherwise.
    """
    query = f"SELECT 1 FROM {table} WHERE " + " AND ".join([f"{key} = ?" for key in conditions.keys()])
    cursor = conn.cursor()
    cursor.execute(query, tuple(conditions.values()))
    return cursor.fetchone() is not None


def add_entry(conn: sqlite3.Connection, table: str, **data):
    """
    Add a new entry to the specified table.

    Args:
        conn (sqlite3.Connection): Database connection.
        table (str): Table name.
        data: Column-value pairs to insert.
    """
    columns = ", ".join(data.keys())
    placeholders = ", ".join("?" for _ in data)
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    cursor = conn.cursor()
    try:
        cursor.execute(query, tuple(data.values()))
        conn.commit()
        print(f"Entry added successfully to {table}!")
    except sqlite3.IntegrityError as e:
        print(f"Failed to add entry: {e}")


def add_summary_subtitles(channel_id: str, max_results: int = 7):
    """
    Summarize YouTube subtitles and add them to the database.

    Args:
        channel_id (str): YouTube channel ID.
        max_results (int): Number of videos to fetch.
    """
    with get_connection() as conn:
        video_list = get_video(channel_id=channel_id, max_results=max_results)
        for video in video_list:
            if entry_exists(conn, "yt_summaries", date=video['date'], name=video['name']):
                print(f"An entry for {video['date']} and {video['name']} already exists.")
                continue
            subtitles = get_subtitles(video['video_id'])
            summarized_text = synthesize_video_with_llm(subtitles[:8000])
            add_entry(conn, "yt_summaries", date=video['date'], name=video['name'], text=summarized_text)


def add_entry_info():
    """
    Add the latest scan information to the database.
    """
    with get_connection() as conn:
        article = parse_dexerto_anime()[0]
        if entry_exists(conn, "scan_info", scan=article['scan']):
            print("Scan information already exists.")
            return

        details = parse_dexerto(article['url'])
        summarized_text = synthesize_infos_with_llm(details)
        add_entry(conn, "scan_info", scan=article['scan'], text=summarized_text, title=article['title'])


if __name__ == '__main__':
    # Example usage
    add_entry_info()
    add_summary_subtitles('UCu2e-o9q5_hZgPHCv8m1Qzg', max_results=3)

