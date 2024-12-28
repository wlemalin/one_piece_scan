from flask import Blueprint, render_template, request, abort
from flaskr.db import get_db

bp = Blueprint('dynamic_pages', __name__)

def fetch_page_data(query: str, params: tuple) -> dict:
    """
    Fetch page data from the database using the provided query and parameters.
    
    Args:
        query (str): The SQL query to execute.
        params (tuple): Parameters for the SQL query.
    
    Returns:
        dict: The fetched data as a dictionary, or None if no data is found.
    """
    db = get_db()
    page_data = db.execute(query, params).fetchone()
    return page_data


@bp.route('/<date>/<name>')
def summary_pages(date: str, name: str):
    """
    Display a summary page for a given date and name.
    
    URL example: /2024-09-16/name
    """
    query = 'SELECT text FROM yt_summaries WHERE date = ? AND name = ?'
    page_data = fetch_page_data(query, (date, name))

    if page_data is None:
        abort(404, description=f"No content available for {name} on {date}.")

    return render_template('explanation.html', text=page_data['text'], date=date, name=name)


@bp.route('/<scan>')
def summary_info(scan: str):
    """
    Display summary information for a given scan.
    
    URL example: /12345
    """
    query = 'SELECT text FROM scan_info WHERE scan = ?'
    page_data = fetch_page_data(query, (scan,))

    if page_data is None:
        abort(404, description=f"No content available for scan {scan}.")

    return render_template('explanation.html', text=page_data['text'], scan=scan)
