from flask import Blueprint, render_template, request, redirect, url_for, flash
from flaskr.db import get_db

bp = Blueprint('dynamic_pages', __name__)

@bp.route('/<date>/<name>')
def summary_pages(date, name):
    """
    Show page by date and name.
    
    URL example: /2024-09-16/name
    """
    db = get_db()

    page_data = db.execute(
        'SELECT text FROM entries WHERE date = ? AND name = ?',
        (date, name)
    ).fetchone()

    if page_data is None:
        return f"No content available for {name} on {date}", 404

    return render_template('explanation.html', text=page_data['text'], date=date, name=name)