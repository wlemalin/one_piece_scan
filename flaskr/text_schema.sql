-- add table 'yt_summaries' to stock youtube summaries
CREATE TABLE IF NOT EXISTS yt_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    name TEXT NOT NULL,
    text TEXT NOT NULL,
    link TEXT NOT NULL,
    title TEXT NOT NULL,
    UNIQUE(date, name, text, link, title)
);

-- add index
CREATE INDEX IF NOT EXISTS idx_date_name ON yt_summaries(date, name);

-- add table 'scan_info' to stock last info about scan release 
CREATE TABLE IF NOT EXISTS scan_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan INTEGER NOT NULL UNIQUE,
    text TEXT NOT NULL,
    title TEXT NOT NULL,
    link TEXT NOT NULL
);


-- add table 'weekly_news' to stock the latest twitter news 
CREATE TABLE IF NOT EXISTS weekly_news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week INTEGER NOT NULL UNIQUE,
    news TEXT NOT NULL
);
