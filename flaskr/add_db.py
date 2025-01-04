import sqlite3
import os

if __name__ == '__main__':
    import sys
    script_dir = os.path.join(os.getcwd(), 'flaskr')  
    sys.path.append(script_dir)

from generate.llm_summary import *
from scraping.yt_subtitles import *
from scraping.youtube_api.get_link import *
from scraping.get_latest_scan import *

# Configurations
DATABASE = os.path.join('instance', 'flaskr.sqlite')

def entry_exists(conn, date, name):
    """
    Function to check if an entry with the given date and name already exists in the database.
    
    Args:
        conn (sqlite3.Connection): Database connection.
        date (str): Date in format YYYY-MM-DDTHH:MM:SSZ.
        name (str): Name of the YouTube channel.
        
    Returns:
        bool: True if the entry exists, False otherwise.
    """
    cursor = conn.cursor()
    cursor.execute(
        'SELECT 1 FROM yt_summaries WHERE date = ? AND name = ?',
        (date, name)
    )
    return cursor.fetchone() is not None

def add_entry(conn, date, name, text):
    """
    Function to add a new entry to the database if it doesn't already exist.
    
    Args: 
        conn (sqlite3.Connection): Database connection.
        date (str): Date in format YYYY-MM-DDTHH:MM:SSZ.
        name (str): Name of the YouTube channel.
        text (str): Generated text.
    """
    if entry_exists(conn, date, name):
        print(f"An entry with {date} date and {name} already exists.\n\n\n")
        return

    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO yt_summaries (date, name, text) VALUES (?, ?, ?)',
            (date, name, text)
        )
        conn.commit()
        print(f"Entry added successfully! test local link http://127.0.0.1:5000/{date}/{name}")
    except sqlite3.IntegrityError as e:
        print(f"Failed to add entry: {e}")

def add_summary_subtitles(channel_id:str, max_results:int = 7):
    """
    Function to summarize and add this to the database.

    Args:
        channel_id: id of a youtube channel.
    """
    conn = sqlite3.connect(DATABASE)
    
    try:
        video_list = get_video(channel_id=channel_id, max_results=max_results)
        for video in video_list: 
            if entry_exists(conn, video['date'], video['name']):
                print(f"An entry with {video['date']} and {video['name']} already exists.\n\n\n")
                continue         
            text = get_subtitles(video['video_id'])
            text = synthesize_video_with_llm(text[:8000])
            add_entry(conn, video['date'], video['name'], text)
    finally:
        conn.close()

def check_entry_info(conn, scan): 
    cursor = conn.cursor()
    cursor.execute(
        'SELECT 1 FROM scan_info WHERE scan = ?',
        (scan,)
    )
    return cursor.fetchone() is not None

def add_entry_info():
    conn = sqlite3.connect(DATABASE)
    article = parse_dexerto_anime(9)[0]

    if check_entry_info(conn, article['scan']):
        print('Une information sur la sortie du scan existe déjà')
        return
    
    text = parse_dexerto(article['url'])
    text = synthesize_infos_with_llm(text)
    cursor = conn.cursor()

    try:
        cursor.execute(
            'INSERT INTO scan_info (scan, text, title) VALUES (?, ?, ?)',
            (article['scan'], text, article['title'])
        )
        conn.commit()
        print(f"Entry added successfully!")
    except sqlite3.IntegrityError as e:
        print(f"Failed to add entry: {e}")

# Example usage
if __name__ == '__main__':
    # article = parse_dexerto_anime()[0]
    # text = parse_dexerto(article['url'])
    # text = synthesize_infos_with_llm(text)
    # print(type(text))
    # add_entry_info()
    add_summary_subtitles('UCu2e-o9q5_hZgPHCv8m1Qzg', 3)

