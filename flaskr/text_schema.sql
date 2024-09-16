-- add table 'entries' to stock text
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    name TEXT NOT NULL,
    text TEXT NOT NULL,
    UNIQUE(date, name, text)
);

-- add index
CREATE INDEX IF NOT EXISTS idx_date_name ON entries(date, name);
