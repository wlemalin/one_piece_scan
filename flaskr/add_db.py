import sqlite3
import os
import click

if __name__ == '__main__':
    import sys
    script_dir = os.path.join(os.getcwd(), 'flaskr')  # Chemin absolu vers 'flaskr'
    sys.path.append(script_dir)

from generate.llm_summary import *
from scraping.yt_subtitles import *
from scraping.youtube_api.get_link import *

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
        'SELECT 1 FROM entries WHERE date = ? AND name = ?',
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
        print("An entry with this date and name already exists.")
        return

    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO entries (date, name, text) VALUES (?, ?, ?)',
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
                print(f"An entry with {video['date']} date and {video['name']} already exists.\n\n\n")
                continue
            
            text = get_subtitles(video['video_id'])
            text = synthesize_video_with_llm(text[:8000])
            add_entry(conn, video['date'], video['name'], text)
    finally:
        conn.close()

@click.command('add_summary_subtitles')
@click.argument('max_results', type=int)
def add_to_db():
    """Add data"""
    add_summary_subtitles('UCu2e-o9q5_hZgPHCv8m1Qzg', 3)
    click.echo('added')

# Example usage
if __name__ == '__main__':

    add_summary_subtitles('UCu2e-o9q5_hZgPHCv8m1Qzg', 3)

