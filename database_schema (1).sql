-- Cricbuzz LiveStats
-- SQLite Database Schema and Sample Data
-- Sample data is for demonstration only.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL UNIQUE,
    country TEXT
);

CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    team_id INTEGER,
    role TEXT,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team1_id INTEGER,
    team2_id INTEGER,
    match_date DATE,
    format TEXT,
    venue TEXT,
    status TEXT,
    winner_team_id INTEGER,
    FOREIGN KEY (team1_id) REFERENCES teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES teams(team_id),
    FOREIGN KEY (winner_team_id) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS player_stats (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    match_id INTEGER NOT NULL,
    runs INTEGER DEFAULT 0,
    wickets INTEGER DEFAULT 0,
    balls_faced INTEGER DEFAULT 0,
    overs_bowled REAL DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

-- Sample teams
INSERT OR IGNORE INTO teams (team_name, country)
VALUES
    ('India', 'India'),
    ('Australia', 'Australia'),
    ('England', 'England');

-- Sample players
INSERT INTO players (player_name, team_id, role)
SELECT 'Virat Kohli', team_id, 'Batter'
FROM teams
WHERE team_name = 'India'
AND NOT EXISTS (
    SELECT 1 FROM players WHERE player_name = 'Virat Kohli'
);

INSERT INTO players (player_name, team_id, role)
SELECT 'Rohit Sharma', team_id, 'Batter'
FROM teams
WHERE team_name = 'India'
AND NOT EXISTS (
    SELECT 1 FROM players WHERE player_name = 'Rohit Sharma'
);

INSERT INTO players (player_name, team_id, role)
SELECT 'Pat Cummins', team_id, 'Bowler'
FROM teams
WHERE team_name = 'Australia'
AND NOT EXISTS (
    SELECT 1 FROM players WHERE player_name = 'Pat Cummins'
);

INSERT INTO players (player_name, team_id, role)
SELECT 'Joe Root', team_id, 'Batter'
FROM teams
WHERE team_name = 'England'
AND NOT EXISTS (
    SELECT 1 FROM players WHERE player_name = 'Joe Root'
);

-- Sample match for SQL practice (not live match data)
INSERT INTO matches (
    team1_id, team2_id, match_date, format, venue, status
)
SELECT
    t1.team_id,
    t2.team_id,
    '2026-10-20',
    'ODI',
    'Sample Cricket Ground',
    'Completed'
FROM teams t1
JOIN teams t2
    ON t2.team_name = 'Australia'
WHERE t1.team_name = 'India'
AND NOT EXISTS (
    SELECT 1 FROM matches
    WHERE team1_id = t1.team_id
      AND team2_id = t2.team_id
      AND match_date = '2026-10-20'
      AND venue = 'Sample Cricket Ground'
);

-- Sample player statistics
INSERT INTO player_stats (
    player_id, match_id, runs, wickets, balls_faced, overs_bowled
)
SELECT
    p.player_id, m.match_id, 75, 0, 60, 0
FROM players p
JOIN teams t ON t.team_id = p.team_id
JOIN matches m ON m.team1_id = t.team_id
WHERE p.player_name = 'Virat Kohli'
  AND m.venue = 'Sample Cricket Ground'
  AND NOT EXISTS (
      SELECT 1 FROM player_stats ps
      WHERE ps.player_id = p.player_id
        AND ps.match_id = m.match_id
  );
