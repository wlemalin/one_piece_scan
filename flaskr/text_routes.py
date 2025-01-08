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
        'SELECT text FROM yt_summaries WHERE date = ? AND name = ?',
        (date, name)
    ).fetchone()

    if page_data is None:
        return f"No content available for {name} on {date}", 404

    return render_template('explanation.html', text=page_data['text'], date=date, name=name)

@bp.route('/<scan>')
def summary_info(scan):
    db = get_db()

    page_data = db.execute(
        'SELECT text FROM scan_info WHERE scan = ?',
        (scan,)
    ).fetchone()

    if page_data is None:
        return f"No content available for {scan}", 404

    return render_template('explanation.html', text=page_data['text'], scan=scan)

@bp.route('/theories')
def index_theories():
    db = get_db()
    cur = db.execute('SELECT name, link, title FROM yt_summaries')
    entries = cur.fetchall()

    return render_template('theories.html', entries=entries)

@bp.route('/info')
def index_info():
    db = get_db()
    cur = db.execute('SELECT scan, link FROM scan_info')
    entries = cur.fetchall()

    return render_template('info.html', entries=entries)

@bp.route('/')
def home():
    return render_template('release_status.html')
