-- add table 'yt_summaries' to stock youtube summaries
CREATE TABLE IF NOT EXISTS yt_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    name TEXT NOT NULL,
    text TEXT NOT NULL,
    UNIQUE(date, name, text)
);

-- add index
CREATE INDEX IF NOT EXISTS idx_date_name ON yt_summaries(date, name);
