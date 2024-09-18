import sqlite3
import os

if __name__ == '__main__':
    import sys
    script_dir = os.path.join(os.getcwd(), 'flaskr')  # Chemin absolu vers 'flaskr'
    sys.path.append(script_dir)

from generate.llm_summary import *
from scraping.yt_subtitles import *
from scraping.youtube_api.get_link import *

# Configurations
DATABASE = os.path.join('instance', 'flaskr.sqlite')

def add_entry(date, name, text):
    """
    Function to add new entry in database.

    Args: 
        date: add date with format YYYY-MM-DD
        name: name of the youtube channel
        text: generated text
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO entries (date, name, text) VALUES (?, ?, ?)',
            (date, name, text)
        )
        conn.commit()
        print("Entry added successfully!")
    except sqlite3.IntegrityError:
        print("An entry with this date and name already exists.")
    finally:
        conn.close()

def add_summary_subtitles(channel_id:str):
    """
    Function to summarize and add this to the database.

    Args:
        channel_id: id of a youtube channel.
    """
    video_id = get_last_video(channel_id=channel_id)
    text = get_subtitles(video_id)
    text = synthesize_video_with_llm(text[:8000])
    add_entry('2024-09-16', 'montcorvo', text)

# Example usage
if __name__ == '__main__':
    # Replace these with actual values
    # add_entry('1996-03-09', 'JohnDoe', 'Un nasique sauvage apparait.')
    
    # def get_db_test():
           
    #     instance_path = os.path.join(os.path.dirname(__name__), 'instance')
    #     database_path = os.path.join(instance_path, 'flaskr.sqlite')

    #     db = sqlite3.connect(
    #         database_path,
    #         detect_types=sqlite3.PARSE_DECLTYPES
    #     )
    #     db.row_factory = sqlite3.Row

    #     return db

    
    # def show_page_by_date_and_name(date, name):

    #     db = get_db_test()

    #     page_data = db.execute(
    #         'SELECT text FROM entries WHERE date = ? AND name = ?',
    #         (date, name)
    #     ).fetchone()

    #     if page_data is None:
    #         return f"No content available for {name} on {date}", 404

    #     return f"Content: {page_data['text']}"
    
    # show_page_by_date_and_name('1996-03-09', 'JohnDoe')

    add_summary_subtitles('UCu2e-o9q5_hZgPHCv8m1Qzg')

