# ===== Colab code cell 1 =====
import sys
import platform

print("Python Version:", sys.version)
print("Operating System:", platform.system())
print("Project Name: Cricbuzz LiveStats")
print("Environment Setup: Started")

# ===== Colab code cell 2 =====
import importlib.util

libraries = ["requests", "pandas", "streamlit", "sqlite3"]

for library in libraries:
    available = importlib.util.find_spec(library) is not None
    print(f"{library}: {'Available' if available else 'Not installed'}")

# ===== Colab code cell 3 =====
get_ipython().system('pip install streamlit')

# ===== Colab code cell 4 =====
import streamlit as st

print("Streamlit Version:", st.__version__)
print("Streamlit Installation: Successful")

# ===== Colab code cell 5 =====
import os

folders = [
    "Cricbuzz_LiveStats",
    "Cricbuzz_LiveStats/database",
    "Cricbuzz_LiveStats/sql",
    "Cricbuzz_LiveStats/pages",
    "Cricbuzz_LiveStats/utils",
    "Cricbuzz_LiveStats/docs"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print("Created:", folder)

print("\nProject folder structure created successfully!")

# ===== Colab code cell 6 =====
import os

folders = [
    "Cricbuzz_LiveStats",
    "Cricbuzz_LiveStats/database",
    "Cricbuzz_LiveStats/sql",
    "Cricbuzz_LiveStats/pages",
    "Cricbuzz_LiveStats/utils",
    "Cricbuzz_LiveStats/docs"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print("Created:", folder)

print("\nProject folder structure created successfully!")

# ===== Colab code cell 7 =====
import sqlite3
import os

db_folder = "/content/Cricbuzz_LiveStats/database"
os.makedirs(db_folder, exist_ok=True)

db_path = os.path.join(db_folder, "cricbuzz.db")

connection = sqlite3.connect(db_path)

print("Database created successfully!")
print("Database location:", db_path)

connection.close()

# ===== Colab code cell 8 =====
import sqlite3

db_path = "/content/Cricbuzz_LiveStats/database/cricbuzz.db"

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL UNIQUE,
    country TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    team_id INTEGER,
    role TEXT,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
)
""")

cursor.execute("""
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
)
""")

cursor.execute("""
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
)
""")

connection.commit()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type = 'table'
AND name NOT LIKE 'sqlite_%'
ORDER BY name
""")

print("Tables created successfully:")
for row in cursor.fetchall():
    print("-", row[0])

connection.close()

# ===== Colab code cell 9 =====
import sqlite3

db_path = "/content/Cricbuzz_LiveStats/database/cricbuzz.db"

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Insert sample teams
cursor.executemany("""
INSERT OR IGNORE INTO teams (team_name, country)
VALUES (?, ?)
""", [
    ("India", "India"),
    ("Australia", "Australia"),
    ("England", "England")
])

# Get team IDs
cursor.execute("SELECT team_id, team_name FROM teams")
teams = {name: team_id for team_id, name in cursor.fetchall()}

# Insert sample players
cursor.executemany("""
INSERT INTO players (player_name, team_id, role)
SELECT ?, ?, ?
WHERE NOT EXISTS (
    SELECT 1 FROM players WHERE player_name = ?
)
""", [
    ("Virat Kohli", teams["India"], "Batter", "Virat Kohli"),
    ("Rohit Sharma", teams["India"], "Batter", "Rohit Sharma"),
    ("Pat Cummins", teams["Australia"], "Bowler", "Pat Cummins"),
    ("Joe Root", teams["England"], "Batter", "Joe Root")
])

connection.commit()

# Display inserted data
cursor.execute("""
SELECT p.player_name, t.team_name, p.role
FROM players p
LEFT JOIN teams t ON p.team_id = t.team_id
ORDER BY p.player_id
""")

print("Sample player data:")
for row in cursor.fetchall():
    print(row)

connection.close()

# ===== Colab code cell 10 =====
import requests
import json
from getpass import getpass

# API Key নিরাপদে ইনপুট নাও
API_KEY = getpass("Enter your Cricket API Key: ")

# Cricket API endpoint
url = "https://api.cricapi.com/v1/currentMatches"

params = {
    "apikey": API_KEY,
    "offset": 0
}

try:
    response = requests.get(url, params=params, timeout=30)

    print("HTTP Status:", response.status_code)

    data = response.json()

    # API response দেখো
    print(json.dumps(data, indent=2)[:8000])

except requests.exceptions.RequestException as e:
    print("Connection Error:", e)

except ValueError:
    print("Response JSON নয়:")
    print(response.text[:2000])

# ===== Colab code cell 11 =====
import requests
import json

# আগের API request-এর response variable যদি response হয়
data = response.json()

print("Response type:", type(data))
print("Available keys:")

if isinstance(data, dict):
    print(list(data.keys()))

print("\nResponse preview:")
print(json.dumps(data, indent=2)[:5000])

# ===== Colab code cell 12 =====
import requests
import json
from getpass import getpass

# তোমার API key নিরাপদে দাও
api_key = getpass("Enter your CricketData API key: ")

url = "https://api.cricapi.com/v1/currentMatches"

params = {
    "apikey": api_key,
    "offset": 0
}

response = requests.get(url, params=params, timeout=30)

print("HTTP Status:", response.status_code)

if response.status_code == 200:
    result = response.json()

    print("API Status:", result.get("status"))
    print("Response keys:", list(result.keys()))

    matches = result.get("data", [])

    print("Total matches:", len(matches))

    for match in matches[:10]:
        print("\nMatch:", match.get("name"))
        print("Status:", match.get("status"))
        print("Venue:", match.get("venue"))
        print("Score:", match.get("score", []))
else:
    print(response.text[:1000])

# ===== Colab code cell 13 =====
import pandas as pd

matches = result.get("data", [])

rows = []

for match in matches:
    scores = match.get("score", [])

    team_scores = []
    for score in scores:
        team = score.get("inning", "Team")
        runs = score.get("r", 0)
        wickets = score.get("w", 0)
        overs = score.get("o", 0)

        team_scores.append(
            f"{team}: {runs}/{wickets} ({overs} overs)"
        )

    rows.append({
        "Match": match.get("name", "N/A"),
        "Match Type": match.get("matchType", "N/A"),
        "Status": match.get("status", "N/A"),
        "Venue": match.get("venue", "N/A"),
        "Score": " | ".join(team_scores) or "Score unavailable"
    })

df = pd.DataFrame(rows)

display(df)

# ===== Colab code cell 14 =====
for i, match in enumerate(result.get("data", [])[:5]):
    print(f"\n--- Match {i + 1} ---")
    print("Name:", match.get("name"))
    print("Match Type:", match.get("matchType"))
    print("Series:", match.get("series"))
    print("Status:", match.get("status"))
    print("Teams:", match.get("teams"))
    print("Score:", match.get("score"))

# ===== Colab code cell 15 =====
import json

print(json.dumps(result["data"][0], indent=2))

# ===== Colab code cell 16 =====
import pandas as pd
from IPython.display import display, HTML
import html

# আগের API Cell থেকে পাওয়া result ব্যবহার করছি
matches = result.get("data", [])

def get_score(match):
    scores = match.get("score") or []
    if not scores:
        return "Score not available"

    output = []
    for s in scores:
        inning = s.get("inning", "Innings")
        runs = s.get("r", 0)
        wickets = s.get("w", 0)
        overs = s.get("o", 0)

        output.append(
            f"{inning}: {runs}/{wickets} ({overs} overs)"
        )

    return " | ".join(output)

# Match Table-এর জন্য Data তৈরি
rows = []

for match in matches:
    rows.append({
        "Match": match.get("name", "N/A"),
        "Match Type": match.get("matchType", "N/A"),
        "Status": match.get("status", "N/A"),
        "Venue": match.get("venue", "N/A"),
        "Date": match.get("date", "N/A"),
        "Score": get_score(match)
    })

df = pd.DataFrame(rows)

# Dashboard-এর Match Cards তৈরি
cards = ""

for match in matches:
    name = html.escape(str(match.get("name", "Unknown Match")))
    match_type = html.escape(str(match.get("matchType", "Cricket")))
    status = html.escape(str(match.get("status", "Status unavailable")))
    venue = html.escape(str(match.get("venue", "Venue unavailable")))
    date = html.escape(str(match.get("date", "Date unavailable")))
    score = html.escape(get_score(match))

    cards += f"""
    <div class="match-card">
        <div class="match-type">{match_type}</div>
        <h3>{name}</h3>
        <div class="score">{score}</div>
        <p><b>Status:</b> {status}</p>
        <p>📍 {venue}</p>
        <p>📅 {date}</p>
    </div>
    """

# Website-style Dashboard
dashboard = f"""
<style>
.cricket-dashboard {{
    font-family: Arial, sans-serif;
    background: #0b1220;
    color: white;
    padding: 20px;
    border-radius: 16px;
}}
.hero {{
    background: linear-gradient(120deg, #075e45, #162b53);
    padding: 25px;
    border-radius: 14px;
    margin-bottom: 20px;
}}
.hero h1 {{
    margin: 0 0 8px;
    font-size: 28px;
}}
.hero p {{
    margin: 0;
    color: #d4e6e0;
}}
.stats {{
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
}}
.stat {{
    flex: 1;
    background: #192438;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}}
.stat strong {{
    display: block;
    color: #6ee7a8;
    font-size: 26px;
}}
.match-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 14px;
}}
.match-card {{
    background: #192438;
    border: 1px solid #34445c;
    border-radius: 13px;
    padding: 16px;
    overflow-wrap: anywhere;
}}
.match-card h3 {{
    font-size: 17px;
    line-height: 1.5;
}}
.match-type {{
    color: #6ee7a8;
    font-size: 12px;
    text-transform: uppercase;
}}
.score {{
    color: #6ee7a8;
    font-weight: bold;
    line-height: 1.7;
}}
.match-card p {{
    color: #d1dbea;
    font-size: 13px;
    line-height: 1.6;
}}
</style>

<div class="cricket-dashboard">
    <div class="hero">
        <h1>🏏 Cricket Live Score</h1>
        <p>Your Cricket Dashboard</p>
    </div>

    <div class="stats">
        <div class="stat">
            <strong>{len(matches)}</strong>
            <span>Total Matches</span>
        </div>
    </div>

    <h2>Match Cards</h2>
    <div class="match-grid">
        {cards if cards else "No matches available"}
    </div>
</div>
"""

display(HTML(dashboard))

print("CRICKET MATCH TABLE")
display(df)

# ===== Colab code cell 17 =====
import requests
import pandas as pd
from IPython.display import display, HTML
from google.colab import output
import html
import json

# API key আবার নিরাপদে দাও
# আগের Cell-এ api_key variable থাকলে এই লাইনটি বাদ দিতে পারো
from getpass import getpass
if "api_key" not in globals() or not api_key:
    api_key = getpass("Enter CricketData API key: ")

def fetch_matches():
    url = "https://api.cricapi.com/v1/currentMatches"
    params = {"apikey": api_key, "offset": 0}

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "success":
        raise ValueError("API response সফল হয়নি।")

    return data.get("data", [])

def score_text(match):
    scores = match.get("score") or []
    if not scores:
        return "Score not available"

    parts = []
    for s in scores:
        parts.append(
            f"{s.get('inning', 'Innings')}: "
            f"{s.get('r', '?')}/{s.get('w', '?')} "
            f"({s.get('o', '?')} overs)"
        )
    return " | ".join(parts)

def render_dashboard(matches):
    records = []
    cards = []

    for m in matches:
        name = str(m.get("name", "Unknown match"))
        status = str(m.get("status", "Status unavailable"))
        match_type = str(m.get("matchType", "Unknown"))
        venue = str(m.get("venue", "Venue unavailable"))
        date = str(m.get("date", ""))
        score = score_text(m)

        records.append({
            "Match": name,
            "Type": match_type,
            "Status": status,
            "Venue": venue,
            "Date": date,
            "Score": score
        })

        safe = lambda value: html.escape(str(value))

        cards.append(f"""
        <article class="match-card"
          data-search="{safe(name + ' ' + status + ' ' + venue + ' ' + match_type).lower()}"
          data-status="{safe(status).lower()}">
          <span class="type">{safe(match_type)}</span>
          <h3>{safe(name)}</h3>
          <div class="score">{safe(score)}</div>
          <p>{safe(status)}</p>
          <small>📍 {safe(venue)}</small><br>
          <small>📅 {safe(date)}</small>
        </article>
        """)

    table = pd.DataFrame(records)

    page = f"""
    <style>
    .dash {{font-family:Arial,sans-serif;background:#0b1220;color:#f1f5f9;
      padding:20px;border-radius:16px}}
    .hero {{background:linear-gradient(120deg,#075e45,#172554);
      padding:22px;border-radius:13px}}
    .hero h2 {{margin:0 0 8px}}
    .tools {{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0}}
    .tools input,.tools select,.tools button {{padding:11px;border-radius:8px;
      border:1px solid #475569;font-size:14px}}
    .tools input {{flex:1;min-width:170px}}
    .tools button {{background:#16a34a;color:white;cursor:pointer}}
    .grid {{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));
      gap:13px}}
    .match-card {{background:#172337;border:1px solid #334155;
      padding:15px;border-radius:12px;overflow-wrap:anywhere}}
    .match-card h3 {{font-size:16px;line-height:1.5}}
    .type {{color:#86efac;font-size:12px;text-transform:uppercase}}
    .score {{color:#86efac;font-weight:bold;line-height:1.7}}
    .match-card p {{color:#dbeafe;line-height:1.5}}
    .match-card small {{color:#a5b4c8;line-height:1.8}}
    #count {{color:#a5f3c5;margin:12px 0}}
    </style>

    <div class="dash">
      <div class="hero">
        <h2>🏏 Cricket Live Score Dashboard</h2>
        <p>Search matches, filter results and refresh API data.</p>
      </div>

      <div class="tools">
        <input id="searchMatch" placeholder="Search team or match...">
        <select id="statusFilter">
          <option value="all">All Matches</option>
          <option value="live">Live / In Progress</option>
          <option value="completed">Completed</option>
          <option value="upcoming">Upcoming / Other</option>
        </select>
        <button onclick="filterMatches()">Search / Filter</button>
      </div>

      <div id="count">Showing {len(matches)} matches</div>
      <div class="grid" id="matchGrid">
        {''.join(cards)}
      </div>
    </div>

    <script>
    function filterMatches() {{
      const query = document.getElementById('searchMatch').value.toLowerCase();
      const filter = document.getElementById('statusFilter').value;
      const cards = document.querySelectorAll('#matchGrid .match-card');
      let visible = 0;

      cards.forEach(card => {{
        const text = card.dataset.search;
        const status = card.dataset.status;
        const isLive = /live|in progress|innings|stumps/.test(status);
        const isComplete = /won|result|complete|draw|tied/.test(status);
        let show = text.includes(query);

        if (filter === 'live') show = show && isLive;
        if (filter === 'completed') show = show && isComplete;
        if (filter === 'upcoming') show = show && !isLive && !isComplete;

        card.style.display = show ? '' : 'none';
        if (show) visible++;
      }});

      document.getElementById('count').textContent =
        'Showing ' + visible + ' matches';
    }}
    document.getElementById('searchMatch').addEventListener('input', filterMatches);
    document.getElementById('statusFilter').addEventListener('change', filterMatches);
    </script>
    """

    display(HTML(page))
    print("MATCH TABLE")
    display(table)

# Fetch fresh data, then render the dashboard and table
try:
    latest_matches = fetch_matches()
    render_dashboard(latest_matches)
except Exception as error:
    print("Dashboard refresh failed:", error)
    print("আগের API Cell এবং API key ঠিক আছে কি না পরীক্ষা করো।")

# ===== Colab code cell 18 =====
import requests
import pandas as pd
import html
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
from getpass import getpass

# 1. API Key check
if "api_key" not in globals() or not api_key:
    api_key = getpass("Enter your CricketData API key: ")

# 2. Fetch match data
def fetch_matches():
    url = "https://api.cricapi.com/v1/currentMatches"
    params = {"apikey": api_key, "offset": 0}

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "success":
        raise ValueError("API failed: " + str(data.get("info", data.get("status"))))

    return data.get("data", [])

matches = fetch_matches()

# 3. Dashboard controls
search_box = widgets.Text(
    placeholder="Search team, venue or match...",
    description="Search:",
    layout=widgets.Layout(width="70%")
)

status_filter = widgets.Dropdown(
    options=["All Matches", "Live", "Upcoming", "Completed"],
    value="All Matches",
    description="Status:"
)

refresh_button = widgets.Button(
    description="↻ Refresh Scores",
    button_style="success",
    icon="refresh"
)

dashboard_output = widgets.Output()

def safe(value):
    return html.escape(str(value if value is not None else ""))

def get_category(match):
    if match.get("matchEnded") is True:
        return "Completed"
    if match.get("matchStarted") is True:
        return "Live"
    return "Upcoming"

def get_scores(match):
    scores = match.get("score") or []
    if not scores:
        return "Score not available"

    parts = []
    for s in scores:
        team = s.get("inning", "")
        runs = s.get("r", "?")
        wickets = s.get("w", "?")
        overs = s.get("o", "?")
        parts.append(
            f"{team}: {runs}/{wickets} ({overs} overs)"
        )
    return " | ".join(parts)

# 4. Render dashboard
def render_dashboard(*args):
    query = search_box.value.strip().lower()
    selected_status = status_filter.value

    filtered = []
    for match in matches:
        category = get_category(match)
        searchable = " ".join([
            str(match.get("name", "")),
            str(match.get("venue", "")),
            str(match.get("status", "")),
            " ".join(match.get("teams") or [])
        ]).lower()

        if query and query not in searchable:
            continue
        if selected_status != "All Matches" and category != selected_status:
            continue
        filtered.append(match)

    with dashboard_output:
        clear_output(wait=True)

        live_count = sum(
            1 for m in matches if get_category(m) == "Live"
        )

        display(HTML(f"""
        <div style="background:#101827;color:white;padding:24px;
                    border-radius:16px;font-family:Arial,sans-serif;">
          <h1 style="margin:0;color:#60a5fa;">
            🏏 Cricket Live Score
          </h1>
          <p style="color:#cbd5e1;margin-bottom:20px;">
            Your Cricket Match Centre
          </p>
          <div style="display:flex;gap:12px;flex-wrap:wrap;">
            <div style="background:#1e293b;padding:16px;border-radius:12px;flex:1;min-width:110px;">
              <div style="color:#94a3b8;">Total Matches</div>
              <h2 style="margin:8px 0;">{len(matches)}</h2>
            </div>
            <div style="background:#1e293b;padding:16px;border-radius:12px;flex:1;min-width:110px;">
              <div style="color:#94a3b8;">Live Matches</div>
              <h2 style="margin:8px 0;color:#4ade80;">{live_count}</h2>
            </div>
            <div style="background:#1e293b;padding:16px;border-radius:12px;flex:1;min-width:110px;">
              <div style="color:#94a3b8;">Search Results</div>
              <h2 style="margin:8px 0;">{len(filtered)}</h2>
            </div>
          </div>
        </div>
        """))

        if not filtered:
            display(HTML("""
            <p style="padding:20px;font-family:Arial;">
              No matches found. Try another search or filter.
            </p>
            """))
            return

        cards = []
        for m in filtered:
            category = get_category(m)
            teams = m.get("teams") or []
            team_text = " vs ".join(teams) if teams else m.get("name", "Match")
            scores = get_scores(m)

            badge_color = {
                "Live": "#16a34a",
                "Upcoming": "#2563eb",
                "Completed": "#64748b"
            }.get(category, "#64748b")

            cards.append(f"""
            <div style="background:white;border:1px solid #e2e8f0;
                        border-radius:14px;padding:18px;
                        box-shadow:0 3px 10px #00000008;">
              <div style="display:flex;justify-content:space-between;
                          gap:8px;align-items:center;flex-wrap:wrap;">
                <span style="font-size:12px;color:#64748b;">
                  {safe(m.get("matchType", "Cricket"))}
                </span>
                <span style="background:{badge_color};color:white;
                             padding:5px 10px;border-radius:20px;
                             font-size:12px;">
                  {safe(category)}
                </span>
              </div>
              <h3 style="color:#0f172a;margin:16px 0 10px;">
                {safe(team_text)}
              </h3>
              <div style="background:#f1f5f9;padding:12px;
                          border-radius:8px;color:#0f172a;">
                <b>Score</b><br>{safe(scores)}
              </div>
              <p style="color:#334155;margin-bottom:5px;">
                <b>Status:</b> {safe(m.get("status", "Not available"))}
              </p>
              <p style="color:#64748b;font-size:13px;margin-bottom:5px;">
                📍 {safe(m.get("venue", "Venue not available"))}
              </p>
              <p style="color:#64748b;font-size:13px;">
                📅 {safe(m.get("date", "Date not available"))}
              </p>
            </div>
            """)

        display(HTML(f"""
        <div style="display:grid;
                    grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
                    gap:16px;margin-top:18px;">
          {''.join(cards)}
        </div>
        """))

        # Table view
        rows = []
        for m in filtered:
            rows.append({
                "Teams": " vs ".join(m.get("teams") or []),
                "Type": m.get("matchType", ""),
                "Status": get_category(m),
                "Score": get_scores(m),
                "Venue": m.get("venue", ""),
                "Date": m.get("date", "")
            })

        display(HTML("<h3 style='margin-top:24px'>Match Data Table</h3>"))
        display(pd.DataFrame(rows))

def refresh_scores(button):
    with dashboard_output:
        clear_output(wait=True)
        display(HTML("<p>Refreshing match data...</p>"))

    try:
        global matches
        matches = fetch_matches()
        render_dashboard()
    except Exception as e:
        with dashboard_output:
            clear_output(wait=True)
            display(HTML(
                "<p style='color:#dc2626'>Refresh failed: "
                + safe(e) + "</p>"
            ))

search_box.observe(render_dashboard, names="value")
status_filter.observe(render_dashboard, names="value")
refresh_button.on_click(refresh_scores)

display(widgets.HBox([search_box, status_filter, refresh_button]))
display(dashboard_output)
render_dashboard()

# ===== Colab code cell 19 =====
import threading
import requests
import pandas as pd
import html
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
from getpass import getpass

# 1. API Key check
if "api_key" not in globals() or not api_key:
    api_key = getpass("Enter your CricketData API key: ")

# 2. Fetch match data
def fetch_matches():
    url = "https://api.cricapi.com/v1/currentMatches"
    params = {"apikey": api_key, "offset": 0}

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "success":
        raise ValueError("API failed: " + str(data.get("info", data.get("status"))))

    return data.get("data", [])

matches = fetch_matches()

# 3. Dashboard controls
search_box = widgets.Text(
    placeholder="Search team, venue or match...",
    description="Search:",
    layout=widgets.Layout(width="70%")
)

status_filter = widgets.Dropdown(
    options=["All Matches", "Live", "Upcoming", "Completed"],
    value="All Matches",
    description="Status:"
)

refresh_button = widgets.Button(
    description="↻ Refresh Scores",
    button_style="success",
    icon="refresh"
)

dashboard_output = widgets.Output()

def safe(value):
    return html.escape(str(value if value is not None else ""))

def get_category(match):
    if match.get("matchEnded") is True:
        return "Completed"
    if match.get("matchStarted") is True:
        return "Live"
    return "Upcoming"

def get_scores(match):
    scores = match.get("score") or []
    if not scores:
        return "Score not available"

    parts = []
    for s in scores:
        team = s.get("inning", "")
        runs = s.get("r", "?")
        wickets = s.get("w", "?")
        overs = s.get("o", "?")
        parts.append(
            f"{team}: {runs}/{wickets} ({overs} overs)"
        )
    return " | ".join(parts)

# 4. Render dashboard
def render_dashboard(*args):
    query = search_box.value.strip().lower()
    selected_status = status_filter.value

    filtered = []
    for match in matches:
        category = get_category(match)
        searchable = " ".join([
            str(match.get("name", "")),
            str(match.get("venue", "")),
            str(match.get("status", "")),
            " ".join(match.get("teams") or [])
        ]).lower()

        if query and query not in searchable:
            continue
        if selected_status != "All Matches" and category != selected_status:
            continue
        filtered.append(match)

    with dashboard_output:
        clear_output(wait=True)

        live_count = sum(
            1 for m in matches if get_category(m) == "Live"
        )

        display(HTML(f"""
        <div style="background:#101827;color:white;padding:24px;
                    border-radius:16px;font-family:Arial,sans-serif;">
          <h1 style="margin:0;color:#60a5fa;">
            🏏 Cricket Live Score
          </h1>
          <p style="color:#cbd5e1;margin-bottom:20px;">
            Your Cricket Match Centre
          </p>
          <div style="display:flex;gap:12px;flex-wrap:wrap;">
            <div style="background:#1e293b;padding:16px;border-radius:12px;flex:1;min-width:110px;">
              <div style="color:#94a3b8;">Total Matches</div>
              <h2 style="margin:8px 0;">{len(matches)}</h2>
            </div>
            <div style="background:#1e293b;padding:16px;border-radius:12px;flex:1;min-width:110px;">
              <div style="color:#94a3b8;">Live Matches</div>
              <h2 style="margin:8px 0;color:#4ade80;">{live_count}</h2>
            </div>
            <div style="background:#1e293b;padding:16px;border-radius:12px;flex:1;min-width:110px;">
              <div style="color:#94a3b8;">Search Results</div>
              <h2 style="margin:8px 0;">{len(filtered)}</h2>
            </div>
          </div>
        </div>
        """))

        if not filtered:
            display(HTML("""
            <p style="padding:20px;font-family:Arial;">
              No matches found. Try another search or filter.
            </p>
            """))
            return

        cards = []
        for m in filtered:
            category = get_category(m)
            teams = m.get("teams") or []
            team_text = " vs ".join(teams) if teams else m.get("name", "Match")
            scores = get_scores(m)

            badge_color = {
                "Live": "#16a34a",
                "Upcoming": "#2563eb",
                "Completed": "#64748b"
            }.get(category, "#64748b")

            cards.append(f"""
            <div style="background:white;border:1px solid #e2e8f0;
                        border-radius:14px;padding:18px;
                        box-shadow:0 3px 10px #00000008;">
              <div style="display:flex;justify-content:space-between;
                          gap:8px;align-items:center;flex-wrap:wrap;">
                <span style="font-size:12px;color:#64748b;">
                  {safe(m.get("matchType", "Cricket"))}
                </span>
                <span style="background:{badge_color};color:white;
                             padding:5px 10px;border-radius:20px;
                             font-size:12px;">
                  {safe(category)}
                </span>
              </div>
              <h3 style="color:#0f172a;margin:16px 0 10px;">
                {safe(team_text)}
              </h3>
              <div style="background:#f1f5f9;padding:12px;
                          border-radius:8px;color:#0f172a;">
                <b>Score</b><br>{safe(scores)}
              </div>
              <p style="color:#334155;margin-bottom:5px;">
                <b>Status:</b> {safe(m.get("status", "Not available"))}
              </p>
              <p style="color:#64748b;font-size:13px;margin-bottom:5px;">
                📍 {safe(m.get("venue", "Venue not available"))}
              </p>
              <p style="color:#64748b;font-size:13px;">
                📅 {safe(m.get("date", "Date not available"))}
              </p>
            </div>
            """)

        display(HTML(f"""
        <div style="display:grid;
                    grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
                    gap:16px;margin-top:18px;">
          {''.join(cards)}
        </div>
        """))

        # Table view
        rows = []
        for m in filtered:
            rows.append({
                "Teams": " vs ".join(m.get("teams") or []),
                "Type": m.get("matchType", ""),
                "Status": get_category(m),
                "Score": get_scores(m),
                "Venue": m.get("venue", ""),
                "Date": m.get("date", "")
            })

        display(HTML("<h3 style='margin-top:24px'>Match Data Table</h3>"))
        display(pd.DataFrame(rows))

def refresh_scores(button):
    with dashboard_output:
        clear_output(wait=True)
        display(HTML("<p>Refreshing match data...</p>"))

    try:
        global matches
        matches = fetch_matches()
        render_dashboard()
    except Exception as e:
        with dashboard_output:
            clear_output(wait=True)
            display(HTML(
                "<p style='color:#dc2626'>Refresh failed: "
                + safe(e) + "</p>"
            ))

search_box.observe(render_dashboard, names="value")
status_filter.observe(render_dashboard, names="value")
refresh_button.on_click(refresh_scores)

display(widgets.HBox([search_box, status_filter, refresh_button]))
display(dashboard_output)
render_dashboard()
# Auto Refresh Settings
AUTO_REFRESH_SECONDS = 120  # 2 minutes
auto_refresh_enabled = False
auto_refresh_timer = None

def auto_refresh():
    global auto_refresh_timer

    if not auto_refresh_enabled:
        return

    try:
        global matches
        matches = fetch_matches()
        render_dashboard()
    except Exception as e:
        with dashboard_output:
            display(HTML(
                "<p style='color:#dc2626'>"
                "Auto refresh failed: " + safe(e) + "</p>"
            ))

    if auto_refresh_enabled:
        auto_refresh_timer = threading.Timer(
            AUTO_REFRESH_SECONDS, auto_refresh
        )
        auto_refresh_timer.daemon = True
        auto_refresh_timer.start()

def start_auto_refresh(button):
    global auto_refresh_enabled
    if not auto_refresh_enabled:
        auto_refresh_enabled = True
        auto_refresh()

def stop_auto_refresh(button):
    global auto_refresh_enabled, auto_refresh_timer
    auto_refresh_enabled = False

    if auto_refresh_timer is not None:
        auto_refresh_timer.cancel()

    with dashboard_output:
        display(HTML("<p>Auto Refresh stopped.</p>"))

start_button = widgets.Button(
    description="Start Auto Refresh",
    button_style="success"
)

stop_button = widgets.Button(
    description="Stop Auto Refresh",
    button_style="warning"
)

start_button.on_click(start_auto_refresh)
stop_button.on_click(stop_auto_refresh)

display(widgets.HBox([start_button, stop_button]))

# ===== Colab code cell 20 =====
# ==========================================
# Cricket Dashboard: Enhanced Features
# Auto Refresh + Last Updated + Live Highlight
# ==========================================

import threading
from datetime import datetime
from IPython.display import display, HTML
import ipywidgets as widgets

# Settings
AUTO_REFRESH_SECONDS = 120
auto_refresh_enabled = False
auto_refresh_timer = None
last_updated = "Not updated yet"

# Enhanced dashboard renderer
def render_dashboard_enhanced(*args):
    query = search_box.value.strip().lower()
    selected_status = status_filter.value

    filtered = []

    for match in matches:
        category = get_category(match)

        searchable = " ".join([
            str(match.get("name", "")),
            str(match.get("venue", "")),
            str(match.get("status", "")),
            " ".join(match.get("teams") or [])
        ]).lower()

        if query and query not in searchable:
            continue

        if selected_status != "All Matches" and category != selected_status:
            continue

        filtered.append(match)

    with dashboard_output:
        clear_output(wait=True)

        live_count = sum(
            1 for m in matches
            if get_category(m) == "Live"
        )

        display(HTML(f"""
        <div style="background:#101827;color:white;
                    padding:22px;border-radius:15px;
                    font-family:Arial,sans-serif;">
            <h1 style="color:#60a5fa;margin-top:0;">
                🏏 Cricket Live Score Dashboard
            </h1>

            <p style="color:#cbd5e1;">
                Last Updated: {safe(last_updated)}
            </p>

            <div style="display:flex;gap:12px;flex-wrap:wrap;">
                <div style="background:#1e293b;padding:14px;
                            border-radius:10px;flex:1;">
                    Total Matches
                    <h2>{len(matches)}</h2>
                </div>

                <div style="background:#1e293b;padding:14px;
                            border-radius:10px;flex:1;">
                    Live Matches
                    <h2 style="color:#4ade80;">{live_count}</h2>
                </div>

                <div style="background:#1e293b;padding:14px;
                            border-radius:10px;flex:1;">
                    Search Results
                    <h2>{len(filtered)}</h2>
                </div>
            </div>
        </div>
        """))

        if not filtered:
            display(HTML(
                "<p>No matches found. Try another search or filter.</p>"
            ))
            return

        cards = []

        for m in filtered:
            category = get_category(m)
            teams = m.get("teams") or []
            team_text = " vs ".join(teams) if teams else m.get(
                "name", "Match"
            )

            badge_color = {
                "Live": "#16a34a",
                "Upcoming": "#2563eb",
                "Completed": "#64748b"
            }.get(category, "#64748b")

            live_label = (
                '<span style="color:#dc2626;font-weight:bold;">'
                '🔴 LIVE NOW</span>'
                if category == "Live" else
                f'<span style="color:{badge_color};font-weight:bold;">'
                f'{safe(category)}</span>'
            )

            cards.append(f"""
            <div style="background:white;
                        border:1px solid #e2e8f0;
                        border-radius:14px;padding:18px;
                        box-shadow:0 3px 10px #00000010;">

                <div style="display:flex;justify-content:space-between;
                            align-items:center;gap:8px;flex-wrap:wrap;">
                    <span style="color:#64748b;font-size:12px;">
                        {safe(m.get("matchType", "Cricket"))}
                    </span>
                    {live_label}
                </div>

                <h3 style="color:#0f172a;margin-top:16px;">
                    {safe(team_text)}
                </h3>

                <div style="background:#f1f5f9;padding:13px;
                            border-radius:9px;color:#0f172a;">
                    <b>Score</b><br>
                    {safe(get_scores(m))}
                </div>

                <p style="color:#334155;">
                    <b>Status:</b>
                    {safe(m.get("status", "Not available"))}
                </p>

                <p style="color:#64748b;font-size:13px;">
                    📍 {safe(m.get("venue", "Venue not available"))}
                </p>

                <p style="color:#64748b;font-size:13px;">
                    📅 {safe(m.get("date", "Date not available"))}
                </p>
            </div>
            """)

        display(HTML(f"""
        <div style="display:grid;
                    grid-template-columns:repeat(
                        auto-fit,minmax(280px,1fr));
                    gap:16px;margin-top:18px;">
            {''.join(cards)}
        </div>
        """))

        rows = [{
            "Teams": " vs ".join(m.get("teams") or []),
            "Type": m.get("matchType", ""),
            "Status": get_category(m),
            "Score": get_scores(m),
            "Venue": m.get("venue", ""),
            "Date": m.get("date", "")
        } for m in filtered]

        display(HTML("<h3>Match Data Table</h3>"))
        display(pd.DataFrame(rows))


# Stop any previous timer
def stop_existing_timer():
    global auto_refresh_enabled, auto_refresh_timer

    auto_refresh_enabled = False

    if auto_refresh_timer is not None:
        auto_refresh_timer.cancel()
        auto_refresh_timer = None


# Auto refresh worker
def auto_refresh_worker():
    global matches, last_updated, auto_refresh_timer

    if not auto_refresh_enabled:
        return

    try:
        new_matches = fetch_matches()
        matches = new_matches
        last_updated = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        render_dashboard_enhanced()

    except Exception as e:
        with dashboard_output:
            display(HTML(
                '<p style="color:#dc2626;">'
                'Refresh failed: ' + safe(e) + '</p>'
            ))

    finally:
        if auto_refresh_enabled:
            auto_refresh_timer = threading.Timer(
                AUTO_REFRESH_SECONDS,
                auto_refresh_worker
            )
            auto_refresh_timer.daemon = True
            auto_refresh_timer.start()


# Start and stop buttons
start_auto_button = widgets.Button(
    description="Start Auto Refresh",
    button_style="success",
    icon="play"
)

stop_auto_button = widgets.Button(
    description="Stop Auto Refresh",
    button_style="warning",
    icon="stop"
)

manual_refresh_button = widgets.Button(
    description="Refresh Now",
    button_style="info",
    icon="refresh"
)


def start_auto(button):
    global auto_refresh_enabled

    if auto_refresh_enabled:
        return

    auto_refresh_enabled = True
    auto_refresh_worker()


def stop_auto(button):
    stop_existing_timer()
    render_dashboard_enhanced()


def manual_refresh(button):
    global matches, last_updated

    manual_refresh_button.disabled = True

    try:
        matches = fetch_matches()
        last_updated = datetime.now().strftime(
            "%d-%m-%Y %I:%M:%S %p"
        )
        render_dashboard_enhanced()

    except Exception as e:
        with dashboard_output:
            display(HTML(
                '<p style="color:#dc2626;">'
                'Refresh failed: ' + safe(e) + '</p>'
            ))

    finally:
        manual_refresh_button.disabled = False


# Prevent duplicate event handlers on these new buttons
start_auto_button.on_click(start_auto)
stop_auto_button.on_click(stop_auto)
manual_refresh_button.on_click(manual_refresh)

# Reuse the existing search and filter widgets
search_box.unobserve(render_dashboard, names="value")
status_filter.unobserve(render_dashboard, names="value")

search_box.observe(render_dashboard_enhanced, names="value")
status_filter.observe(render_dashboard_enhanced, names="value")

# Initial display
display(widgets.HBox([
    start_auto_button,
    stop_auto_button,
    manual_refresh_button
]))

render_dashboard_enhanced()

# ===== Colab code cell 21 =====
print("Total matches:", len(matches))

for m in matches[:10]:
    print("Match:", m.get("name"))
    print("Started:", m.get("matchStarted"))
    print("Ended:", m.get("matchEnded"))
    print("Status:", m.get("status"))
    print("-" * 40)

# ===== Colab code cell 22 =====
for m in matches[:10]:
    print("Match:", m.get("name"))
    print("Started:", m.get("matchStarted"))
    print("Ended:", m.get("matchEnded"))
    print("Status:", m.get("status"))
    print("Score:", m.get("score"))
    print("=" * 60)

# ===== Colab code cell 23 =====
def get_category(match):
    status = str(match.get("status") or "").strip().lower()

    started = match.get("matchStarted")
    ended = match.get("matchEnded")

    # Completed match detection
    completed_keywords = [
        "won by",
        "draw",
        "tied",
        "no result",
        "abandoned",
        "match drawn",
        "match tied",
        "result"
    ]

    if ended is True or any(
        keyword in status for keyword in completed_keywords
    ):
        return "Completed"

    # Live match detection
    if started is True and ended is not True:
        return "Live"

    # Upcoming match detection
    if started is False:
        return "Upcoming"

    return "Upcoming"


# Refresh dashboard using updated status detection
render_dashboard_enhanced()

# ===== Colab code cell 24 =====
def get_category(match):
    status = str(match.get("status") or "").strip().lower()

    started = match.get("matchStarted")
    ended = match.get("matchEnded")

    # Completed match detection
    completed_keywords = [
        "won by",
        "draw",
        "tied",
        "no result",
        "abandoned",
        "match drawn",
        "match tied",
        "result"
    ]

    if ended is True or any(
        keyword in status for keyword in completed_keywords
    ):
        return "Completed"

    # Live match detection
    if started is True and ended is not True:
        return "Live"

    # Upcoming match detection
    if started is False:
        return "Upcoming"

    return "Upcoming"


# Refresh dashboard using updated status detection
render_dashboard_enhanced()

# ===== Colab code cell 25 =====
def get_category(match):
    status = str(match.get("status") or "").strip().lower()

    started = match.get("matchStarted")
    ended = match.get("matchEnded")

    # Completed match detection
    completed_keywords = [
        "won by",
        "draw",
        "tied",
        "no result",
        "abandoned",
        "match drawn",
        "match tied",
        "result"
    ]

    if ended is True or any(
        keyword in status for keyword in completed_keywords
    ):
        return "Completed"

    # Live match detection
    if started is True and ended is not True:
        return "Live"

    # Upcoming match detection
    if started is False:
        return "Upcoming"

    return "Upcoming"


# Refresh dashboard using updated status detection
render_dashboard_enhanced()

# ===== Colab code cell 26 =====
def get_category(match):
    status = str(match.get("status") or "").strip().lower()

    started = match.get("matchStarted")
    ended = match.get("matchEnded")

    # Completed match detection
    completed_keywords = [
        "won by",
        "draw",
        "tied",
        "no result",
        "abandoned",
        "match drawn",
        "match tied",
        "result"
    ]

    if ended is True or any(
        keyword in status for keyword in completed_keywords
    ):
        return "Completed"

    # Live match detection
    if started is True and ended is not True:
        return "Live"

    # Upcoming match detection
    if started is False:
        return "Upcoming"

    return "Upcoming"


# Refresh dashboard using updated status detection
render_dashboard_enhanced()

# ===== Colab code cell 27 =====
def get_category(match):
    status = str(match.get("status") or "").strip().lower()

    started = match.get("matchStarted")
    ended = match.get("matchEnded")

    # Completed match detection
    completed_keywords = [
        "won by",
        "draw",
        "tied",
        "no result",
        "abandoned",
        "match drawn",
        "match tied",
        "result"
    ]

    if ended is True or any(
        keyword in status for keyword in completed_keywords
    ):
        return "Completed"

    # Live match detection
    if started is True and ended is not True:
        return "Live"

    # Upcoming match detection
    if started is False:
        return "Upcoming"

    return "Upcoming"


# Refresh dashboard using updated status detection
render_dashboard_enhanced()

# ===== Colab code cell 28 =====
print("Total matches:", len(matches))
print("Dashboard output:", dashboard_output is not None)

for m in matches[:5]:
    print("Match:", m.get("name"))
    print("Status:", m.get("status"))
    print("Category:", get_category(m))

print("Dashboard renderer exists:",
      "render_dashboard_enhanced" in globals())

# ===== Colab code cell 29 =====
render_dashboard_enhanced()

# ===== Colab code cell 30 =====
render_dashboard_enhanced()

# ===== Colab code cell 31 =====
render_dashboard_enhanced()

# ===== Colab code cell 32 =====
render_dashboard_enhanced()

# ===== Colab code cell 33 =====
render_dashboard_enhanced()

# ===== Colab code cell 34 =====
render_dashboard_enhanced()

# ===== Colab code cell 35 =====
from IPython.display import display, HTML, clear_output

print("Dashboard test started")

with dashboard_output:
    clear_output(wait=True)
    display(HTML("""
        <div style="background:#101827;color:white;
                    padding:25px;border-radius:15px;">
            <h2 style="color:#60a5fa;">
                🏏 Cricket Live Score Dashboard
            </h2>
            <p>Dashboard output is working!</p>
        </div>
    """))

display(dashboard_output)

# ===== Colab code cell 36 =====
# Restore the enhanced dashboard display

try:
    print("Total matches:", len(matches))

    if "render_dashboard_enhanced" in globals():
        render_dashboard_enhanced()
        print("Enhanced dashboard function executed.")
    else:
        print("Enhanced renderer not found.")
        render_dashboard()

except Exception as e:
    print("Dashboard error:", repr(e))

# ===== Colab code cell 37 =====
from datetime import datetime

last_updated = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

print("Last Updated:", last_updated)
print("Total Matches:", len(matches))

print("\nMatch Status Summary:")

for category in ["Live", "Upcoming", "Completed"]:
    count = sum(
        1 for match in matches
        if get_category(match) == category
    )
    print(f"{category}: {count}")

# ===== Colab code cell 38 =====
# Inspect the actual API status for all matches

for i, match in enumerate(matches, start=1):
    print(f"\nMatch {i}: {match.get('name', 'Unknown')}")
    print("Status:", match.get("status", "Not available"))
    print("Started:", match.get("matchStarted"))
    print("Ended:", match.get("matchEnded"))
    print("Date:", match.get("date", "Not available"))

# ===== Colab code cell 39 =====
def get_category(match):
    status = str(match.get("status") or "").strip().lower()
    started = match.get("matchStarted")
    ended = match.get("matchEnded")

    completed_phrases = [
        "won by",
        "match tied",
        "match drawn",
        "drawn",
        "no result",
        "abandoned",
        "cancelled"
    ]

    if ended is True or any(
        phrase in status for phrase in completed_phrases
    ):
        return "Completed"

    if started is True and ended is not True:
        return "Live"

    if started is False:
        return "Upcoming"

    return "Unknown"


render_dashboard_enhanced()

# ===== Colab code cell 40 =====
print("===== CRICKET DASHBOARD CHECK =====")

print("Total Matches:", len(matches))

live_matches = [
    m for m in matches if get_category(m) == "Live"
]

completed_matches = [
    m for m in matches if get_category(m) == "Completed"
]

upcoming_matches = [
    m for m in matches if get_category(m) == "Upcoming"
]

print("Live Matches:", len(live_matches))
print("Completed Matches:", len(completed_matches))
print("Upcoming Matches:", len(upcoming_matches))

print("\n===== RECENT MATCH RESULTS =====")

for match in completed_matches[:5]:
    print("Match:", match.get("name"))
    print("Result:", match.get("status"))
    print("Date:", match.get("date"))
    print("-" * 40)

# ===== Colab code cell 41 =====
from IPython.display import display, HTML
import html

def show_recent_results():
    completed = [
        m for m in matches
        if get_category(m) == "Completed"
    ]

    cards = []

    for m in completed[:10]:
        name = html.escape(str(m.get("name") or "Match"))
        result = html.escape(
            str(m.get("status") or "Result unavailable")
        )
        date = html.escape(str(m.get("date") or "Date unavailable"))
        venue = html.escape(
            str(m.get("venue") or "Venue unavailable")
        )

        cards.append(f"""
        <div style="
            background:white;
            border:1px solid #e2e8f0;
            border-radius:14px;
            padding:18px;
            margin-bottom:14px;
            box-shadow:0 3px 10px #00000010;
        ">
            <div style="color:#64748b;font-size:12px;">
                COMPLETED MATCH
            </div>
            <h3 style="color:#0f172a;margin:10px 0;">
                🏏 {name}
            </h3>
            <p style="color:#15803d;font-weight:bold;">
                🏆 {result}
            </p>
            <p style="color:#475569;">📅 {date}</p>
            <p style="color:#64748b;">📍 {venue}</p>
        </div>
        """)

    if not cards:
        display(HTML("<p>No completed match results available.</p>"))
        return

    display(HTML(f"""
    <div style="
        background:#f8fafc;
        padding:20px;
        border-radius:16px;
        font-family:Arial,sans-serif;
    ">
        <h2 style="color:#0f172a;">
            🏆 Recent Cricket Results
        </h2>
        <p style="color:#64748b;">
            Showing the latest 10 results from the available API data.
        </p>
        {''.join(cards)}
    </div>
    """))

show_recent_results()

# ===== Colab code cell 42 =====
from IPython.display import display, HTML
import html
import pandas as pd

def show_professional_scoreboard():
    cards = []

    for match in matches:
        category = get_category(match)
        teams = match.get("teams") or []
        scores = match.get("score") or []

        team1 = html.escape(str(teams[0])) if len(teams) > 0 else "Team 1"
        team2 = html.escape(str(teams[1])) if len(teams) > 1 else "Team 2"

        score_lines = []

        for score in scores:
            inning = html.escape(str(score.get("inning", "Innings")))
            runs = score.get("r", "-")
            wickets = score.get("w", "-")
            overs = score.get("o", "-")

            score_lines.append(
                f"""
                <div style="display:flex;justify-content:space-between;
                            padding:10px 0;border-bottom:1px solid #e2e8f0;">
                    <span>{inning}</span>
                    <b>{runs}/{wickets} ({overs} overs)</b>
                </div>
                """
            )

        score_html = "".join(score_lines) if score_lines else (
            '<p style="color:#64748b;">Score not available</p>'
        )

        status = html.escape(str(match.get("status") or category))
        venue = html.escape(str(match.get("venue") or "Venue unavailable"))
        date = html.escape(str(match.get("date") or "Date unavailable"))
        match_type = html.escape(str(match.get("matchType") or "Cricket"))

        badge_colors = {
            "Live": "#16a34a",
            "Completed": "#64748b",
            "Upcoming": "#2563eb"
        }
        badge_color = badge_colors.get(category, "#64748b")

        cards.append(f"""
        <div style="background:white;border-radius:16px;
                    padding:20px;border:1px solid #e2e8f0;
                    box-shadow:0 4px 14px #0f172a10;">

            <div style="display:flex;justify-content:space-between;
                        align-items:center;gap:10px;flex-wrap:wrap;">
                <span style="color:#64748b;font-size:12px;">
                    {match_type.upper()}
                </span>
                <span style="background:{badge_color};color:white;
                             padding:5px 10px;border-radius:20px;
                             font-size:12px;">
                    {category.upper()}
                </span>
            </div>

            <div style="text-align:center;padding:18px 0;">
                <h3 style="color:#0f172a;margin:5px 0;">{team1}</h3>
                <div style="color:#94a3b8;font-weight:bold;">VS</div>
                <h3 style="color:#0f172a;margin:5px 0;">{team2}</h3>
            </div>

            <div style="background:#f8fafc;border-radius:10px;
                        padding:12px;color:#0f172a;">
                <b>INNINGS SCOREBOARD</b>
                {score_html}
            </div>

            <p style="color:#15803d;font-weight:600;margin-top:14px;">
                🏆 {status}
            </p>

            <p style="color:#64748b;font-size:13px;">
                📅 {date}
            </p>
            <p style="color:#64748b;font-size:13px;">
                📍 {venue}
            </p>
        </div>
        """)

    if not cards:
        display(HTML("<p>No match data available.</p>"))
        return

    display(HTML(f"""
    <div style="background:#f1f5f9;padding:22px;
                border-radius:18px;font-family:Arial,sans-serif;">
        <h1 style="color:#0f172a;margin-top:0;">
            🏏 Professional Cricket Scoreboard
        </h1>
        <p style="color:#64748b;">
            Total Matches: {len(matches)}
        </p>
        <div style="display:grid;
                    grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
                    gap:18px;">
            {''.join(cards)}
        </div>
    </div>
    """))

show_professional_scoreboard()

# ===== Colab code cell 43 =====
# ==========================================================
# COMPLETE CRICKET LIVE SCORE DASHBOARD
# Google Colab | CricAPI / CricketData
# ==========================================================

import requests
import pandas as pd
import html
import threading
from datetime import datetime
from getpass import getpass
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output

# ---------------- 1. CONFIGURATION ----------------

API_URL = "https://api.cricapi.com/v1/currentMatches"
AUTO_REFRESH_SECONDS = 120

if "api_key" not in globals() or not api_key:
    api_key = getpass("Enter your CricketData/CricAPI API key: ")

matches = []
last_updated = "Not updated yet"
last_error = ""
auto_refresh_enabled = False
auto_refresh_timer = None
dashboard_open = False

# ---------------- 2. FETCH MATCH DATA ----------------

def fetch_matches():
    response = requests.get(
        API_URL,
        params={"apikey": api_key, "offset": 0},
        timeout=30
    )
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "success":
        raise ValueError(
            data.get("info", "Unable to fetch match data")
        )

    return data.get("data", [])

# ---------------- 3. MATCH STATUS ----------------

def get_category(match):
    status = str(match.get("status") or "").strip().lower()
    started = match.get("matchStarted")
    ended = match.get("matchEnded")

    completed_words = [
        "won by", "match tied", "match drawn",
        "no result", "abandoned", "cancelled",
        "drawn", "innings victory"
    ]

    if ended is True or any(
        word in status for word in completed_words
    ):
        return "Completed"

    if started is True and ended is not True:
        return "Live"

    if started is False:
        return "Upcoming"

    return "Unknown"

# ---------------- 4. HELPER FUNCTIONS ----------------

def safe(value):
    return html.escape(str(value if value is not None else ""))

def get_teams(match):
    teams = match.get("teams") or []

    if isinstance(teams, list) and teams:
        return [str(team) for team in teams]

    name = str(match.get("name") or "Unknown Match")
    return [name]

def get_scores(match):
    scores = match.get("score") or []

    if not scores:
        return "Score not available"

    parts = []

    for score in scores:
        inning = score.get("inning", "Innings")
        runs = score.get("r", "-")
        wickets = score.get("w", "-")
        overs = score.get("o", "-")

        parts.append(
            f"{inning}: {runs}/{wickets} ({overs} overs)"
        )

    return " | ".join(parts)

# ---------------- 5. DASHBOARD CONTROLS ----------------

search_box = widgets.Text(
    placeholder="Search team, match or venue...",
    description="Search:",
    layout=widgets.Layout(width="100%")
)

status_filter = widgets.Dropdown(
    options=[
        "All Matches", "Live", "Upcoming",
        "Completed", "Unknown"
    ],
    value="All Matches",
    description="Status:",
    layout=widgets.Layout(width="100%")
)

refresh_button = widgets.Button(
    description="Refresh Now",
    icon="refresh",
    button_style="info"
)

start_button = widgets.Button(
    description="Start Auto Refresh",
    icon="play",
    button_style="success"
)

stop_button = widgets.Button(
    description="Stop Auto Refresh",
    icon="stop",
    button_style="warning",
    disabled=True
)

dashboard_output = widgets.Output()

# ---------------- 6. RENDER DASHBOARD ----------------

def render_dashboard(*args):
    query = search_box.value.strip().lower()
    selected = status_filter.value

    filtered = []

    for match in matches:
        category = get_category(match)
        teams = get_teams(match)

        searchable = " ".join([
            str(match.get("name", "")),
            str(match.get("venue", "")),
            str(match.get("status", "")),
            " ".join(teams)
        ]).lower()

        if query and query not in searchable:
            continue

        if selected != "All Matches" and category != selected:
            continue

        filtered.append(match)

    live_count = sum(
        1 for m in matches if get_category(m) == "Live"
    )
    completed_count = sum(
        1 for m in matches if get_category(m) == "Completed"
    )
    upcoming_count = sum(
        1 for m in matches if get_category(m) == "Upcoming"
    )

    cards = []

    for match in filtered:
        teams = get_teams(match)
        category = get_category(match)

        team1 = safe(teams[0])
        team2 = safe(teams[1]) if len(teams) > 1 else ""

        if len(teams) > 2:
            team1 = safe(" vs ".join(teams))

        if team2:
            matchup = f"{team1} <span style='color:#94a3b8'>VS</span> {team2}"
        else:
            matchup = team1

        colors = {
            "Live": "#16a34a",
            "Upcoming": "#2563eb",
            "Completed": "#64748b",
            "Unknown": "#64748b"
        }
        color = colors.get(category, "#64748b")

        score_html = safe(get_scores(match))
        result = safe(match.get("status") or "Status unavailable")
        venue = safe(match.get("venue") or "Venue unavailable")
        date = safe(match.get("date") or "Date unavailable")
        match_type = safe(match.get("matchType") or "Cricket")

        live_label = (
            "🔴 LIVE NOW"
            if category == "Live"
            else category.upper()
        )

        cards.append(f"""
        <div style="
            background:white;
            border:1px solid #e2e8f0;
            border-radius:15px;
            padding:18px;
            box-shadow:0 4px 12px #0000000c;
            min-width:0;
        ">
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                gap:8px;
                flex-wrap:wrap;
            ">
                <span style="color:#64748b;font-size:12px">
                    {match_type.upper()}
                </span>
                <span style="
                    background:{color};
                    color:white;
                    border-radius:20px;
                    padding:5px 9px;
                    font-size:11px;
                    font-weight:bold;
                ">{live_label}</span>
            </div>

            <h3 style="
                text-align:center;
                color:#0f172a;
                margin:20px 0;
                line-height:1.6;
            ">{matchup}</h3>

            <div style="
                background:#f1f5f9;
                color:#0f172a;
                padding:13px;
                border-radius:9px;
                overflow-wrap:anywhere;
            ">
                <b>🏏 SCOREBOARD</b>
                <div style="margin-top:10px;line-height:1.8">
                    {score_html}
                </div>
            </div>

            <p style="color:#15803d;font-weight:600">
                🏆 {result}
            </p>
            <p style="color:#64748b;font-size:13px">
                📅 {date}
            </p>
            <p style="color:#64748b;font-size:13px">
                📍 {venue}
            </p>
        </div>
        """)

    rows = []

    for match in filtered:
        rows.append({
            "Teams": " vs ".join(get_teams(match)),
            "Type": match.get("matchType", ""),
            "Category": get_category(match),
            "Score": get_scores(match),
            "Result / Status": match.get("status", ""),
            "Venue": match.get("venue", ""),
            "Date": match.get("date", "")
        })

    with dashboard_output:
        clear_output(wait=True)

        display(HTML(f"""
        <div style="
            background:#101827;
            color:white;
            padding:24px;
            border-radius:16px;
            font-family:Arial,sans-serif;
        ">
            <h1 style="color:#60a5fa;margin:0">
                🏏 Cricket Live Score
            </h1>
            <p style="color:#cbd5e1">
                Your Complete Cricket Match Centre
            </p>
            <p style="color:#cbd5e1;font-size:13px">
                Last successful update: {safe(last_updated)}
            </p>
            <div style="
                display:grid;
                grid-template-columns:repeat(auto-fit,minmax(120px,1fr));
                gap:10px;
                margin-top:20px;
            ">
                <div style="background:#1e293b;padding:14px;border-radius:10px">
                    <div style="color:#cbd5e1">Total Matches</div>
                    <h2>{len(matches)}</h2>
                </div>
                <div style="background:#1e293b;padding:14px;border-radius:10px">
                    <div style="color:#86efac">Live</div>
                    <h2>{live_count}</h2>
                </div>
                <div style="background:#1e293b;padding:14px;border-radius:10px">
                    <div style="color:#93c5fd">Upcoming</div>
                    <h2>{upcoming_count}</h2>
                </div>
                <div style="background:#1e293b;padding:14px;border-radius:10px">
                    <div style="color:#cbd5e1">Completed</div>
                    <h2>{completed_count}</h2>
                </div>
            </div>
        </div>
        """))

        if last_error:
            display(HTML(f"""
            <div style="background:#fef2f2;color:#991b1b;
                        padding:12px;margin-top:12px;border-radius:8px">
                <b>Refresh warning:</b> {safe(last_error)}
            </div>
            """))

        display(HTML(
            "<h2 style='font-family:Arial;color:#0f172a;"
            "margin-top:24px'>🏆 Match Scoreboards</h2>"
        ))

        if cards:
            display(HTML(f"""
            <div style="
                display:grid;
                grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
                gap:16px;
                font-family:Arial,sans-serif;
            ">
                {''.join(cards)}
            </div>
            """))
        else:
            display(HTML("""
            <p style="padding:15px;color:#64748b">
                No matches found. Try another search or filter.
            </p>
            """))

        display(HTML(
            "<h2 style='font-family:Arial;color:#0f172a;"
            "margin-top:28px'>📋 Match Data Table</h2>"
        ))

        if rows:
            display(pd.DataFrame(rows).reset_index(drop=True))
        else:
            display(HTML("<p>No table data available.</p>"))

        display(HTML("""
        <p style="color:#64748b;font-size:12px;margin-top:16px">
            Scores and results are provided by the connected API.
            Live updates depend on API data availability.
        </p>
        """))

# ---------------- 7. REFRESH FUNCTIONS ----------------

def refresh_data():
    global matches, last_updated, last_error

    new_matches = fetch_matches()
    matches = new_matches
    last_updated = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    last_error = ""

def on_refresh(button):
    refresh_button.disabled = True

    try:
        refresh_data()
    except Exception as error:
        global last_error
        last_error = str(error)

    render_dashboard()
    refresh_button.disabled = False

# ---------------- 8. AUTO REFRESH ----------------

def auto_refresh_worker():
    global auto_refresh_timer, last_error

    if not auto_refresh_enabled:
        return

    try:
        refresh_data()
    except Exception as error:
        last_error = str(error)

    render_dashboard()

    if auto_refresh_enabled:
        auto_refresh_timer = threading.Timer(
            AUTO_REFRESH_SECONDS,
            auto_refresh_worker
        )
        auto_refresh_timer.daemon = True
        auto_refresh_timer.start()

def on_start(button):
    global auto_refresh_enabled

    if auto_refresh_enabled:
        return

    auto_refresh_enabled = True
    start_button.disabled = True
    stop_button.disabled = False

    # First refresh happens immediately.
    auto_refresh_worker()

def on_stop(button):
    global auto_refresh_enabled, auto_refresh_timer

    auto_refresh_enabled = False

    if auto_refresh_timer is not None:
        auto_refresh_timer.cancel()
        auto_refresh_timer = None

    start_button.disabled = False
    stop_button.disabled = True
    render_dashboard()

# ---------------- 9. CONNECT CONTROLS ----------------

search_box.observe(render_dashboard, names="value")
status_filter.observe(render_dashboard, names="value")

refresh_button.on_click(on_refresh)
start_button.on_click(on_start)
stop_button.on_click(on_stop)

# ---------------- 10. INITIALIZE DASHBOARD ----------------

controls = widgets.VBox([
    search_box,
    status_filter,
    widgets.HBox([
        refresh_button,
        start_button,
        stop_button
    ])
])

display(HTML("""
<div style="font-family:Arial,sans-serif;padding:10px 0">
<h2>🏏 Complete Cricket Dashboard</h2>
<p>Search matches, filter results and refresh scores.</p>
</div>
"""))

display(controls)
display(dashboard_output)

try:
    refresh_data()
except Exception as error:
    last_error = str(error)
    print("API Error:", last_error)

render_dashboard()

print("Dashboard initialized.")

# ===== Colab code cell 44 =====
# ============================================================
# CRICKET LIVE SCORE DASHBOARD - ADVANCED COLAB VERSION
# Features: Live Score Cards, Search, Filters, Auto Refresh
# ============================================================

import requests
import pandas as pd
import html
import time
import threading
from datetime import datetime
from getpass import getpass
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output

# 1. API setup
API_URL = "https://api.cricapi.com/v1/currentMatches"

if "api_key" not in globals() or not api_key:
    api_key = getpass("Enter your Cricket API key: ")

matches = []
last_updated = "Not updated yet"
last_error = ""
auto_refresh_enabled = False
auto_refresh_thread = None
refresh_lock = threading.Lock()
auto_refresh_stop = threading.Event()


def safe(value):
    """Safely display text in HTML."""
    if value is None or value == "":
        return "N/A"
    return html.escape(str(value))


# 2. Match status detection
def get_category(match):
    status = str(match.get("status", "")).lower()
    started = match.get("matchStarted", False)
    ended = match.get("matchEnded", False)

    if ended or any(word in status for word in [
        "won by", "draw", "tied", "no result", "abandoned"
    ]):
        return "Completed"

    if started or any(word in status for word in [
        "live", "in progress", "innings break", "stumps",
        "day ", "need ", "trail by"
    ]):
        return "Live"

    return "Upcoming"


# 3. Team names and scores
def get_teams(match):
    teams = match.get("teams") or []
    if isinstance(teams, list) and teams:
        return [str(t) for t in teams]
    return ["Team 1", "Team 2"]


def get_scores(match):
    score_list = match.get("score") or []
    if not isinstance(score_list, list) or not score_list:
        return "Score not available"

    result = []
    for item in score_list:
        if not isinstance(item, dict):
            continue

        inning = item.get("inning", "")
        runs = item.get("r", "?")
        wickets = item.get("w", "?")
        overs = item.get("o", "?")

        result.append(
            f"{inning}: {runs}/{wickets} ({overs} overs)"
            if inning else f"{runs}/{wickets} ({overs} overs)"
        )

    return " | ".join(result) if result else "Score not available"


# 4. Fetch the latest matches
def fetch_matches():
    response = requests.get(
        API_URL,
        params={"apikey": api_key, "offset": 0},
        timeout=25
    )
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "success":
        raise RuntimeError(
            data.get("reason", "API did not return success.")
        )

    result = data.get("data", [])
    if not isinstance(result, list):
        raise RuntimeError("Unexpected match data format.")

    return result


# 5. Dashboard controls
search_box = widgets.Text(
    placeholder="Search team, venue or match...",
    description="Search:",
    layout=widgets.Layout(width="55%")
)

status_filter = widgets.Dropdown(
    options=["All", "Live", "Upcoming", "Completed"],
    value="All",
    description="Status:"
)

type_filter = widgets.Dropdown(
    options=["All"],
    value="All",
    description="Match type:"
)

refresh_button = widgets.Button(
    description="Refresh Scores",
    button_style="primary",
    icon="refresh"
)

start_button = widgets.Button(
    description="Start Auto Refresh",
    button_style="success",
    icon="play"
)

stop_button = widgets.Button(
    description="Stop Auto Refresh",
    button_style="warning",
    icon="stop",
    disabled=True
)

interval_dropdown = widgets.Dropdown(
    options=[
        ("30 seconds", 30),
        ("60 seconds", 60),
        ("120 seconds", 120),
        ("5 minutes", 300)
    ],
    value=120,
    description="Interval:"
)

summary_output = widgets.Output()
cards_output = widgets.Output()
table_output = widgets.Output()
message_output = widgets.Output()


# 6. Filter matches
def get_filtered_matches():
    query = search_box.value.strip().lower()
    chosen_status = status_filter.value
    chosen_type = type_filter.value

    filtered = []

    for match in matches:
        teams = get_teams(match)
        category = get_category(match)
        match_type = str(match.get("matchType", "Unknown")).upper()

        searchable = " ".join([
            str(match.get("name", "")),
            str(match.get("venue", "")),
            str(match.get("status", "")),
            " ".join(teams),
            match_type
        ]).lower()

        if query and query not in searchable:
            continue
        if chosen_status != "All" and category != chosen_status:
            continue
        if chosen_type != "All" and match_type != chosen_type:
            continue

        filtered.append(match)

    return filtered


# 7. Professional dashboard rendering
def render_dashboard():
    filtered = get_filtered_matches()

    with summary_output:
        clear_output(wait=True)
        counts = {
            category: sum(
                1 for m in matches if get_category(m) == category
            )
            for category in ["Live", "Upcoming", "Completed"]
        }

        display(HTML(f"""
        <div style="display:flex;flex-wrap:wrap;gap:12px;margin:12px 0;">
          <div style="background:#172554;color:white;padding:18px;border-radius:12px;min-width:125px;">
            <div>Total Matches</div>
            <div style="font-size:28px;font-weight:bold;">{len(matches)}</div>
          </div>
          <div style="background:#166534;color:white;padding:18px;border-radius:12px;min-width:125px;">
            <div>Live</div>
            <div style="font-size:28px;font-weight:bold;">{counts["Live"]}</div>
          </div>
          <div style="background:#92400e;color:white;padding:18px;border-radius:12px;min-width:125px;">
            <div>Upcoming</div>
            <div style="font-size:28px;font-weight:bold;">{counts["Upcoming"]}</div>
          </div>
          <div style="background:#374151;color:white;padding:18px;border-radius:12px;min-width:125px;">
            <div>Completed</div>
            <div style="font-size:28px;font-weight:bold;">{counts["Completed"]}</div>
          </div>
        </div>
        <div style="color:#64748b;font-size:13px;">
          Last successful update: {safe(last_updated)}
        </div>
        """))

    with cards_output:
        clear_output(wait=True)

        if not filtered:
            display(HTML(
                "<p style='padding:16px;'>No matches found for these filters.</p>"
            ))
        else:
            card_html = ""

            for match in filtered:
                category = get_category(match)
                teams = get_teams(match)
                team_text = " vs ".join(teams)
                match_type = str(match.get("matchType", "Unknown")).upper()
                score_text = get_scores(match)
                status_text = match.get("status", "Status unavailable")
                venue = match.get("venue", "Venue unavailable")
                date = match.get("date", "Date unavailable")

                badge_color = {
                    "Live": "#b91c1c",
                    "Upcoming": "#a16207",
                    "Completed": "#166534"
                }.get(category, "#475569")

                card_html += f"""
                <div style="
                    background:#ffffff;color:#111827;
                    border:1px solid #e5e7eb;border-radius:14px;
                    padding:18px;margin:12px 0;
                    box-shadow:0 3px 10px rgba(0,0,0,.06);
                ">
                  <div style="display:flex;justify-content:space-between;
                              flex-wrap:wrap;gap:8px;">
                    <b>{safe(match_type)} · {safe(match.get("name", team_text))}</b>
                    <span style="background:{badge_color};color:white;
                                 padding:4px 10px;border-radius:20px;font-size:12px;">
                      {safe(category)}
                    </span>
                  </div>
                  <h3 style="margin:14px 0 8px;">{safe(team_text)}</h3>
                  <div style="font-size:15px;font-weight:600;margin-bottom:10px;">
                    {safe(score_text)}
                  </div>
                  <div style="color:#475569;margin:6px 0;">
                    {safe(status_text)}
                  </div>
                  <div style="color:#64748b;font-size:13px;">
                    Venue: {safe(venue)} · Date: {safe(date)}
                  </div>
                </div>
                """

            display(HTML(card_html))

    with table_output:
        clear_output(wait=True)

        rows = []
        for match in filtered:
            rows.append({
                "Match": match.get("name", "Unknown"),
                "Type": match.get("matchType", "Unknown"),
                "Category": get_category(match),
                "Status / Result": match.get("status", "N/A"),
                "Score": get_scores(match),
                "Venue": match.get("venue", "N/A"),
                "Date": match.get("date", "N/A")
            })

        if rows:
            display(pd.DataFrame(rows))
        else:
            print("No data to display.")


# 8. Refresh function
def refresh_data(_=None):
    global matches, last_updated, last_error

    if not refresh_lock.acquire(blocking=False):
        return

    try:
        new_matches = fetch_matches()
        matches = new_matches
        last_updated = datetime.now().strftime("%d %b %Y, %I:%M:%S %p")
        last_error = ""

        available_types = sorted({
            str(m.get("matchType", "Unknown")).upper()
            for m in matches
        })

        current_type = type_filter.value
        type_filter.options = ["All"] + available_types
        type_filter.value = (
            current_type if current_type in available_types else "All"
        )

        with message_output:
            clear_output(wait=True)
            print(f"Updated successfully. {len(matches)} matches loaded.")

    except Exception as exc:
        last_error = str(exc)
        with message_output:
            clear_output(wait=True)
            print("Refresh failed:", last_error)
            print("Check your API key, API plan and internet connection.")

    finally:
        refresh_lock.release()

    render_dashboard()


# 9. Auto-refresh controls
def auto_refresh_worker():
    global auto_refresh_enabled

    while not auto_refresh_stop.is_set():
        wait_seconds = interval_dropdown.value

        if auto_refresh_stop.wait(wait_seconds):
            break

        if auto_refresh_enabled:
            refresh_data()

    auto_refresh_enabled = False
    start_button.disabled = False
    stop_button.disabled = True


def start_auto_refresh(_):
    global auto_refresh_enabled, auto_refresh_thread

    if auto_refresh_enabled:
        return

    auto_refresh_stop.clear()
    auto_refresh_enabled = True
    start_button.disabled = True
    stop_button.disabled = False

    auto_refresh_thread = threading.Thread(
        target=auto_refresh_worker,
        daemon=True
    )
    auto_refresh_thread.start()

    with message_output:
        clear_output(wait=True)
        print(f"Auto refresh started: every {interval_dropdown.value} seconds.")


def stop_auto_refresh(_):
    global auto_refresh_enabled

    auto_refresh_enabled = False
    auto_refresh_stop.set()
    start_button.disabled = False
    stop_button.disabled = True

    with message_output:
        clear_output(wait=True)
        print("Auto refresh stopped.")


refresh_button.on_click(refresh_data)
start_button.on_click(start_auto_refresh)
stop_button.on_click(stop_auto_refresh)

search_box.observe(lambda change: render_dashboard(), names="value")
status_filter.observe(lambda change: render_dashboard(), names="value")
type_filter.observe(lambda change: render_dashboard(), names="value")


# 10. Display the complete dashboard
display(HTML("""
<div style="background:#0f172a;color:white;padding:24px;border-radius:16px;">
  <h1 style="margin:0;">🏏 Cricket Live Score Dashboard</h1>
  <p style="margin-bottom:0;">Scores · Match Status · Search · Auto Refresh</p>
</div>
"""))

display(widgets.HBox([search_box]))
display(widgets.HBox([status_filter, type_filter]))
display(widgets.HBox([refresh_button, interval_dropdown]))
display(widgets.HBox([start_button, stop_button]))
display(message_output)
display(summary_output)

display(HTML("<h3>Match Scoreboard</h3>"))
display(cards_output)

display(HTML("<h3>Match Data Table</h3>"))
display(table_output)

refresh_data()

# ===== Colab code cell 45 =====
# ============================================================
# CRICKET DASHBOARD WEB APP - GRADIO
# Run this cell after Step 1
# ============================================================

get_ipython().run_line_magic('pip', '-q install gradio')

import gradio as gr
from datetime import datetime
import html


def make_web_dashboard(search, status, match_type, refresh_now):
    global matches, last_updated

    # Fetch fresh data when Refresh is clicked
    if refresh_now:
        try:
            matches = fetch_matches()
            last_updated = datetime.now().strftime("%d %b %Y, %I:%M:%S %p")
        except Exception as exc:
            return (
                f"<h3>Could not refresh scores</h3>"
                f"<p>{html.escape(str(exc))}</p>"
            )

    query = (search or "").strip().lower()
    results = []

    for match in matches:
        teams = get_teams(match)
        category = get_category(match)
        mtype = str(match.get("matchType", "Unknown")).upper()

        searchable = " ".join([
            str(match.get("name", "")),
            str(match.get("venue", "")),
            str(match.get("status", "")),
            " ".join(teams),
            mtype
        ]).lower()

        if query and query not in searchable:
            continue
        if status != "All" and category != status:
            continue
        if match_type != "All" and mtype != match_type:
            continue

        results.append(match)

    counts = {
        c: sum(1 for m in matches if get_category(m) == c)
        for c in ["Live", "Upcoming", "Completed"]
    }

    page = f"""
    <div style="font-family:Arial,sans-serif;color:#111827;">
      <div style="background:#0f172a;color:white;padding:24px;
                  border-radius:16px;margin-bottom:16px;">
        <h1 style="margin:0;">🏏 Cricket Live Score</h1>
        <p>Match Centre · Search · Filters</p>
        <small>Last update: {html.escape(str(last_updated))}</small>
      </div>

      <div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:20px;">
        <div style="background:#172554;color:white;padding:16px;border-radius:12px;">
          Total Matches: <b>{len(matches)}</b>
        </div>
        <div style="background:#166534;color:white;padding:16px;border-radius:12px;">
          Live: <b>{counts["Live"]}</b>
        </div>
        <div style="background:#92400e;color:white;padding:16px;border-radius:12px;">
          Upcoming: <b>{counts["Upcoming"]}</b>
        </div>
        <div style="background:#374151;color:white;padding:16px;border-radius:12px;">
          Completed: <b>{counts["Completed"]}</b>
        </div>
      </div>
    """

    if not results:
        page += "<p>No matches found. Try changing your search or filters.</p>"

    for match in results:
        category = get_category(match)
        badge_color = {
            "Live": "#b91c1c",
            "Upcoming": "#a16207",
            "Completed": "#166534"
        }.get(category, "#475569")

        page += f"""
        <div style="border:1px solid #e5e7eb;border-radius:14px;
                    padding:18px;margin:12px 0;background:white;">
          <div style="display:flex;justify-content:space-between;
                      gap:10px;flex-wrap:wrap;">
            <b>{html.escape(str(match.get("matchType", "Unknown")).upper())}
            · {html.escape(str(match.get("name", "Cricket Match")))}</b>
            <span style="background:{badge_color};color:white;
                         padding:4px 10px;border-radius:20px;">
              {category}
            </span>
          </div>
          <h3>{html.escape(" vs ".join(get_teams(match)))}</h3>
          <p><b>{html.escape(get_scores(match))}</b></p>
          <p>{html.escape(str(match.get("status", "Status unavailable")))}</p>
          <small>
            Venue: {html.escape(str(match.get("venue", "N/A")))}
            · Date: {html.escape(str(match.get("date", "N/A")))}
          </small>
        </div>
        """

    page += "</div>"
    return page


with gr.Blocks(title="Cricket Live Score Dashboard") as demo:
    gr.Markdown("# 🏏 Cricket Live Score Dashboard")
    gr.Markdown("Search matches, apply filters and refresh the score feed.")

    with gr.Row():
        web_search = gr.Textbox(
            label="Search",
            placeholder="Team, venue or match name"
        )
        web_status = gr.Dropdown(
            ["All", "Live", "Upcoming", "Completed"],
            value="All",
            label="Match Status"
        )

    web_types = sorted({
        str(m.get("matchType", "Unknown")).upper()
        for m in matches
    })
    web_match_type = gr.Dropdown(
        ["All"] + web_types,
        value="All",
        label="Match Type"
    )

    web_refresh = gr.Button("🔄 Refresh Scores", variant="primary")
    web_output = gr.HTML()

    # Update display when filters change
    web_search.change(
        make_web_dashboard,
        [web_search, web_status, web_match_type, gr.State(False)],
        web_output
    )
    web_status.change(
        make_web_dashboard,
        [web_search, web_status, web_match_type, gr.State(False)],
        web_output
    )
    web_match_type.change(
        make_web_dashboard,
        [web_search, web_status, web_match_type, gr.State(False)],
        web_output
    )
    web_refresh.click(
        make_web_dashboard,
        [web_search, web_status, web_match_type, gr.State(True)],
        web_output
    )

    demo.load(
        make_web_dashboard,
        [web_search, web_status, web_match_type, gr.State(False)],
        web_output
    )

demo.launch(share=True)

# ===== Colab code cell 46 =====
# Website auto-refresh: every 120 seconds
web_timer = gr.Timer(120)

web_timer.tick(
    fn=make_web_dashboard,
    inputs=[
        web_search,
        web_status,
        web_match_type,
        gr.State(True)
    ],
    outputs=web_output
)

# ===== Colab code cell 47 =====
# ============================================================
# CRICKET DASHBOARD WEB APP - GRADIO
# Run this cell after Step 1
# ============================================================

get_ipython().run_line_magic('pip', '-q install gradio')

import gradio as gr
from datetime import datetime
import html


def make_web_dashboard(search, status, match_type, refresh_now):
    global matches, last_updated

    # Fetch fresh data when Refresh is clicked
    if refresh_now:
        try:
            matches = fetch_matches()
            last_updated = datetime.now().strftime("%d %b %Y, %I:%M:%S %p")
        except Exception as exc:
            return (
                f"<h3>Could not refresh scores</h3>"
                f"<p>{html.escape(str(exc))}</p>"
            )

    query = (search or "").strip().lower()
    results = []

    for match in matches:
        teams = get_teams(match)
        category = get_category(match)
        mtype = str(match.get("matchType", "Unknown")).upper()

        searchable = " ".join([
            str(match.get("name", "")),
            str(match.get("venue", "")),
            str(match.get("status", "")),
            " ".join(teams),
            mtype
        ]).lower()

        if query and query not in searchable:
            continue
        if status != "All" and category != status:
            continue
        if match_type != "All" and mtype != match_type:
            continue

        results.append(match)

    counts = {
        c: sum(1 for m in matches if get_category(m) == c)
        for c in ["Live", "Upcoming", "Completed"]
    }

    page = f"""
    <div style="font-family:Arial,sans-serif;color:#111827;">
      <div style="background:#0f172a;color:white;padding:24px;
                  border-radius:16px;margin-bottom:16px;">
        <h1 style="margin:0;">🏏 Cricket Live Score</h1>
        <p>Match Centre · Search · Filters</p>
        <small>Last update: {html.escape(str(last_updated))}</small>
      </div>

      <div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:20px;">
        <div style="background:#172554;color:white;padding:16px;border-radius:12px;">
          Total Matches: <b>{len(matches)}</b>
        </div>
        <div style="background:#166534;color:white;padding:16px;border-radius:12px;">
          Live: <b>{counts["Live"]}</b>
        </div>
        <div style="background:#92400e;color:white;padding:16px;border-radius:12px;">
          Upcoming: <b>{counts["Upcoming"]}</b>
        </div>
        <div style="background:#374151;color:white;padding:16px;border-radius:12px;">
          Completed: <b>{counts["Completed"]}</b>
        </div>
      </div>
    """

    if not results:
        page += "<p>No matches found. Try changing your search or filters.</p>"

    for match in results:
        category = get_category(match)
        badge_color = {
            "Live": "#b91c1c",
            "Upcoming": "#a16207",
            "Completed": "#166534"
        }.get(category, "#475569")

        page += f"""
        <div style="border:1px solid #e5e7eb;border-radius:14px;
                    padding:18px;margin:12px 0;background:white;">
          <div style="display:flex;justify-content:space-between;
                      gap:10px;flex-wrap:wrap;">
            <b>{html.escape(str(match.get("matchType", "Unknown")).upper())}
            · {html.escape(str(match.get("name", "Cricket Match")))}</b>
            <span style="background:{badge_color};color:white;
                         padding:4px 10px;border-radius:20px;">
              {category}
            </span>
          </div>
          <h3>{html.escape(" vs ".join(get_teams(match)))}</h3>
          <p><b>{html.escape(get_scores(match))}</b></p>
          <p>{html.escape(str(match.get("status", "Status unavailable")))}</p>
          <small>
            Venue: {html.escape(str(match.get("venue", "N/A")))}
            · Date: {html.escape(str(match.get("date", "N/A")))}
          </small>
        </div>
        """

    page += "</div>"
    return page


with gr.Blocks(title="Cricket Live Score Dashboard") as demo:
    gr.Markdown("# 🏏 Cricket Live Score Dashboard")
    gr.Markdown("Search matches, apply filters and refresh the score feed.")

    with gr.Row():
        web_search = gr.Textbox(
            label="Search",
            placeholder="Team, venue or match name"
        )
        web_status = gr.Dropdown(
            ["All", "Live", "Upcoming", "Completed"],
            value="All",
            label="Match Status"
        )

    web_types = sorted({
        str(m.get("matchType", "Unknown")).upper()
        for m in matches
    })
    web_match_type = gr.Dropdown(
        ["All"] + web_types,
        value="All",
        label="Match Type"
    )

    web_refresh = gr.Button("🔄 Refresh Scores", variant="primary")
    web_output = gr.HTML()

    # Update display when filters change
    web_search.change(
        make_web_dashboard,
        [web_search, web_status, web_match_type, gr.State(False)],
        web_output
    )
    web_status.change(
        make_web_dashboard,
        [web_search, web_status, web_match_type, gr.State(False)],
        web_output
    )
    web_match_type.change(
        make_web_dashboard,
        [web_search, web_status, web_match_type, gr.State(False)],
        web_output
    )
    web_refresh.click(
        make_web_dashboard,
        [web_search, web_status, web_match_type, gr.State(True)],
        web_output
    )

    demo.load(
        make_web_dashboard,
        [web_search, web_status, web_match_type, gr.State(False)],
        web_output
    )
    # Website auto-refresh: every 120 seconds
web_timer = gr.Timer(120)

web_timer.tick(
    fn=make_web_dashboard,
    inputs=[
        web_search,
        web_status,
        web_match_type,
        gr.State(True)
    ],
    outputs=web_output
)

demo.launch(share=True)

# ===== Colab code cell 48 =====
# ============================================================
# CRICKET DASHBOARD WEB APP - GRADIO
# Run this cell after Step 1
# ============================================================

get_ipython().run_line_magic('pip', '-q install gradio')

import gradio as gr
from datetime import datetime
import html


def make_web_dashboard(search, status, match_type, refresh_now):
    global matches, last_updated

    # Fetch fresh data when Refresh is clicked
    if refresh_now:
        try:
            matches = fetch_matches()
            last_updated = datetime.now().strftime("%d %b %Y, %I:%M:%S %p")
        except Exception as exc:
            return (
                f"<h3>Could not refresh scores</h3>"
                f"<p>{html.escape(str(exc))}</p>"
            )

    query = (search or "").strip().lower()
    results = []

    for match in matches:
        teams = get_teams(match)
        category = get_category(match)
        mtype = str(match.get("matchType", "Unknown")).upper()

        searchable = " ".join([
            str(match.get("name", "")),
            str(match.get("venue", "")),
            str(match.get("status", "")),
            " ".join(teams),
            mtype
        ]).lower()

        if query and query not in searchable:
            continue
        if status != "All" and category != status:
            continue
        if match_type != "All" and mtype != match_type:
            continue

        results.append(match)

    counts = {
        c: sum(1 for m in matches if get_category(m) == c)
        for c in ["Live", "Upcoming", "Completed"]
    }

    page = f"""
    <div style="font-family:Arial,sans-serif;color:#111827;">
      <div style="background:#0f172a;color:white;padding:24px;
                  border-radius:16px;margin-bottom:16px;">
        <h1 style="margin:0;">🏏 Cricket Live Score</h1>
        <p>Match Centre · Search · Filters</p>
        <small>Last update: {html.escape(str(last_updated))}</small>
      </div>

      <div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:20px;">
        <div style="background:#172554;color:white;padding:16px;border-radius:12px;">
          Total Matches: <b>{len(matches)}</b>
        </div>
        <div style="background:#166534;color:white;padding:16px;border-radius:12px;">
          Live: <b>{counts["Live"]}</b>
        </div>
        <div style="background:#92400e;color:white;padding:16px;border-radius:12px;">
          Upcoming: <b>{counts["Upcoming"]}</b>
        </div>
        <div style="background:#374151;color:white;padding:16px;border-radius:12px;">
          Completed: <b>{counts["Completed"]}</b>
        </div>
      </div>
    """

    if not results:
        page += "<p>No matches found. Try changing your search or filters.</p>"

    for match in results:
        category = get_category(match)
        badge_color = {
            "Live": "#b91c1c",
            "Upcoming": "#a16207",
            "Completed": "#166534"
        }.get(category, "#475569")

        page += f"""
        <div style="border:1px solid #e5e7eb;border-radius:14px;
                    padding:18px;margin:12px 0;background:white;">
          <div style="display:flex;justify-content:space-between;
                      gap:10px;flex-wrap:wrap;">
            <b>{html.escape(str(match.get("matchType", "Unknown")).upper())}
            · {html.escape(str(match.get("name", "Cricket Match")))}</b>
            <span style="background:{badge_color};color:white;
                         padding:4px 10px;border-radius:20px;">
              {category}
            </span>
          </div>
          <h3>{html.escape(" vs ".join(get_teams(match)))}</h3>
          <p><b>{html.escape(get_scores(match))}</b></p>
          <p>{html.escape(str(match.get("status", "Status unavailable")))}</p>
          <small>
            Venue: {html.escape(str(match.get("venue", "N/A")))}
            · Date: {html.escape(str(match.get("date", "N/A")))}
          </small>
        </div>
        """

    page += "</div>"
    return page


with gr.Blocks(title="Cricket Live Score Dashboard") as demo:
    gr.Markdown("# 🏏 Cricket Live Score Dashboard")
    gr.Markdown("Search matches, apply filters and refresh the score feed.")

    with gr.Row():
        web_search = gr.Textbox(
            label="Search",
            placeholder="Team, venue or match name"
        )
        web_status = gr.Dropdown(
            ["All", "Live", "Upcoming", "Completed"],
            value="All",
            label="Match Status"
        )

    web_types = sorted({
        str(m.get("matchType", "Unknown")).upper()
        for m in matches
    })
    web_match_type = gr.Dropdown(
        ["All"] + web_types,
        value="All",
        label="Match Type"
    )

    web_refresh = gr.Button("🔄 Refresh Scores", variant="primary")
    web_output = gr.HTML()

    # Update display when filters change
    web_search.change(
        make_web_dashboard,
        [web_search, web_status, web_match_type, gr.State(False)],
        web_output
    )
    web_status.change(
        make_web_dashboard,
        [web_search, web_status, web_match_type, gr.State(False)],
        web_output
    )
    web_match_type.change(
        make_web_dashboard,
        [web_search, web_status, web_match_type, gr.State(False)],
        web_output
    )
    web_refresh.click(
        make_web_dashboard,
        [web_search, web_status, web_match_type, gr.State(True)],
        web_output
    )

    demo.load(
        make_web_dashboard,
        [web_search, web_status, web_match_type, gr.State(False)],
        web_output
    )
    # Auto-refresh every 120 seconds
    web_timer = gr.Timer(value=120, active=True)

    web_timer.tick(
        fn=make_web_dashboard,
        inputs=[
            web_search,
            web_status,
            web_match_type,
            gr.State(True)
        ],
        outputs=[web_output]
    )

demo.launch(share=True)

# ===== Colab code cell 49 =====
# ============================================================
# CRICKET LIVE SCORE DASHBOARD - PROFESSIONAL WEB APP
# Google Colab + Gradio
# Keeps existing backend, search, filters and auto-refresh
# ============================================================

get_ipython().run_line_magic('pip', '-q install gradio')

import gradio as gr
from datetime import datetime
import html

# Keep existing backend functions:
# fetch_matches(), get_teams(), get_category(), get_scores()
# Existing global variables: matches, last_updated


def make_web_dashboard(search, status, match_type, refresh_now):
    global matches, last_updated

    # Fetch fresh scores when requested by button or timer
    if refresh_now:
        try:
            matches = fetch_matches()
            last_updated = datetime.now().strftime(
                "%d %b %Y, %I:%M:%S %p"
            )
        except Exception as exc:
            error_message = html.escape(str(exc))
            return f"""
            <div style="background:#fff1f2;color:#9f1239;
                        padding:24px;border-radius:16px;
                        font-family:Arial,sans-serif;">
                <h2>Unable to refresh scores</h2>
                <p>{error_message}</p>
                <p>Please check your API connection.</p>
            </div>
            """

    query = (search or "").strip().lower()
    results = []

    # Search and filters: preserved
    for match in matches:
        teams = get_teams(match)
        category = get_category(match)
        mtype = str(match.get("matchType", "Unknown")).upper()

        searchable = " ".join([
            str(match.get("name", "")),
            str(match.get("venue", "")),
            str(match.get("status", "")),
            " ".join(teams),
            mtype
        ]).lower()

        if query and query not in searchable:
            continue

        if status != "All" and category != status:
            continue

        if match_type != "All" and mtype != match_type:
            continue

        results.append(match)

    counts = {
        category: sum(
            1 for match in matches
            if get_category(match) == category
        )
        for category in ["Live", "Upcoming", "Completed"]
    }

    # Professional responsive design
    page = """
    <style>
      .cricket-app {
        font-family: Inter, Arial, sans-serif;
        color: #e5e7eb;
        background: #080f1e;
        padding: 18px;
        border-radius: 20px;
      }
      .cricket-hero {
        background: linear-gradient(120deg,#102b4e,#164e63);
        border: 1px solid #24516d;
        border-radius: 18px;
        padding: 26px;
        margin-bottom: 18px;
      }
      .cricket-hero h1 {
        font-size: clamp(25px,4vw,36px);
        margin: 0 0 8px;
        color: white;
      }
      .cricket-muted { color: #a8bfd3; }
      .cricket-stats {
        display: grid;
        grid-template-columns: repeat(4,minmax(0,1fr));
        gap: 12px;
        margin-bottom: 22px;
      }
      .cricket-stat {
        background: #111c30;
        border: 1px solid #25344b;
        border-radius: 14px;
        padding: 17px;
      }
      .cricket-stat-label {
        color: #a8b6ca;
        font-size: 13px;
      }
      .cricket-stat-value {
        font-size: 27px;
        font-weight: 750;
        margin-top: 8px;
        color: white;
      }
      .cricket-section-title {
        font-size: 20px;
        font-weight: 700;
        margin: 22px 0 12px;
        color: white;
      }
      .cricket-match {
        background: #111c30;
        border: 1px solid #293950;
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
        overflow-wrap: anywhere;
      }
      .cricket-match-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
      }
      .cricket-match-name {
        font-weight: 700;
        color: #f3f7ff;
        font-size: 15px;
      }
      .cricket-badge {
        border-radius: 999px;
        padding: 6px 11px;
        font-size: 12px;
        font-weight: 700;
      }
      .cricket-teams {
        font-size: 21px;
        font-weight: 750;
        color: white;
        margin: 20px 0 10px;
      }
      .cricket-score {
        background: #0b1425;
        border-radius: 10px;
        padding: 13px;
        font-size: 18px;
        font-weight: 700;
        color: #93c5fd;
      }
      .cricket-status {
        color: #d2dbea;
        line-height: 1.6;
        margin: 12px 0;
      }
      .cricket-meta {
        color: #9eafc5;
        font-size: 12px;
        line-height: 1.8;
      }
      .cricket-empty {
        padding: 28px;
        text-align: center;
        border: 1px dashed #475569;
        border-radius: 14px;
        color: #cbd5e1;
      }
      @media(max-width:600px) {
        .cricket-app { padding: 10px; }
        .cricket-hero { padding: 19px; }
        .cricket-stats { grid-template-columns: repeat(2,minmax(0,1fr)); }
        .cricket-stat { padding: 13px; }
        .cricket-stat-value { font-size: 23px; }
        .cricket-match { padding: 15px; }
        .cricket-teams { font-size: 18px; }
      }
    </style>
    <div class="cricket-app">
      <div class="cricket-hero">
        <div style="font-size:12px;letter-spacing:2px;
                    color:#a5e6d0;font-weight:700;">
          LIVE CRICKET · MATCH CENTRE
        </div>
        <h1>🏏 Cricket Live Score</h1>
        <p class="cricket-muted">
          Your cricket dashboard for match scores and updates.
        </p>
    """

    page += f"""
        <div class="cricket-muted" style="font-size:12px;">
          Last data refresh: {html.escape(str(last_updated))}
        </div>
      </div>

      <div class="cricket-stats">
        <div class="cricket-stat">
          <div class="cricket-stat-label">TOTAL MATCHES</div>
          <div class="cricket-stat-value">{len(matches)}</div>
        </div>
        <div class="cricket-stat">
          <div class="cricket-stat-label">🔴 LIVE</div>
          <div class="cricket-stat-value" style="color:#f87171;">
            {counts["Live"]}
          </div>
        </div>
        <div class="cricket-stat">
          <div class="cricket-stat-label">📅 UPCOMING</div>
          <div class="cricket-stat-value" style="color:#fbbf24;">
            {counts["Upcoming"]}
          </div>
        </div>
        <div class="cricket-stat">
          <div class="cricket-stat-label">✓ COMPLETED</div>
          <div class="cricket-stat-value" style="color:#6ee7b7;">
            {counts["Completed"]}
          </div>
        </div>
      </div>

      <div class="cricket-section-title">
        Match Centre
        <span style="font-size:13px;color:#9eafc5;font-weight:400;">
          · {len(results)} result(s)
        </span>
      </div>
    """

    if not results:
        page += """
        <div class="cricket-empty">
          <div style="font-size:30px;">🏏</div>
          <h3>No matches found</h3>
          <p>Try another search term or change your filters.</p>
        </div>
        """

    for match in results:
        category = get_category(match)
        teams = " vs ".join(get_teams(match))
        mtype = str(match.get("matchType", "Unknown")).upper()

        badge_colors = {
            "Live": ("#451a1a", "#fca5a5"),
            "Upcoming": ("#422006", "#fcd34d"),
            "Completed": ("#064e3b", "#6ee7b7")
        }
        bg, fg = badge_colors.get(
            category, ("#25344b", "#cbd5e1")
        )

        page += f"""
        <div class="cricket-match">
          <div class="cricket-match-top">
            <div class="cricket-match-name">
              {html.escape(mtype)} ·
              {html.escape(str(match.get("name", "Cricket Match")))}
            </div>
            <span class="cricket-badge"
                  style="background:{bg};color:{fg};">
              {html.escape(str(category))}
            </span>
          </div>

          <div class="cricket-teams">
            {html.escape(teams)}
          </div>

          <div class="cricket-score">
            {html.escape(str(get_scores(match)))}
          </div>

          <div class="cricket-status">
            {html.escape(str(match.get("status", "Status unavailable")))}
          </div>

          <div class="cricket-meta">
            📍 Venue: {html.escape(str(match.get("venue", "N/A")))}
            <br>
            📅 Date: {html.escape(str(match.get("date", "N/A")))}
          </div>
        </div>
        """

    page += """
      <div style="text-align:center;color:#8496ad;
                  font-size:12px;padding:18px 0 4px;">
        Cricket Live Score Dashboard
      </div>
    </div>
    """
    return page


# ============================================================
# WEBSITE INTERFACE
# ============================================================

with gr.Blocks(
    title="Cricket Live Score Dashboard",
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate"
    )
) as demo:

    gr.Markdown(
        "## 🏏 Cricket Live Score Dashboard\n"
        "Search matches, filter results and refresh scores."
    )

    with gr.Row():
        web_search = gr.Textbox(
            label="🔎 Search",
            placeholder="Team, venue or match name",
            scale=2
        )
        web_status = gr.Dropdown(
            choices=["All", "Live", "Upcoming", "Completed"],
            value="All",
            label="Match Status",
            scale=1
        )

    web_types = sorted({
        str(m.get("matchType", "Unknown")).upper()
        for m in matches
    })

    web_match_type = gr.Dropdown(
        choices=["All"] + web_types,
        value="All",
        label="Match Type"
    )

    with gr.Row():
        web_refresh = gr.Button(
            "🔄 Refresh Scores",
            variant="primary"
        )

    web_output = gr.HTML()

    # Reusable state values for event callbacks
    no_refresh = gr.State(value=False)
    do_refresh = gr.State(value=True)

    # Search and filter events: no API call
    web_search.change(
        fn=make_web_dashboard,
        inputs=[
            web_search, web_status,
            web_match_type, no_refresh
        ],
        outputs=web_output
    )

    web_status.change(
        fn=make_web_dashboard,
        inputs=[
            web_search, web_status,
            web_match_type, no_refresh
        ],
        outputs=web_output
    )

    web_match_type.change(
        fn=make_web_dashboard,
        inputs=[
            web_search, web_status,
            web_match_type, no_refresh
        ],
        outputs=web_output
    )

    # Manual refresh
    web_refresh.click(
        fn=make_web_dashboard,
        inputs=[
            web_search, web_status,
            web_match_type, do_refresh
        ],
        outputs=web_output
    )

    # Initial dashboard display
    demo.load(
        fn=make_web_dashboard,
        inputs=[
            web_search, web_status,
            web_match_type, no_refresh
        ],
        outputs=web_output
    )

    # Auto-refresh every 120 seconds
    web_timer = gr.Timer(value=120, active=True)

    web_timer.tick(
        fn=make_web_dashboard,
        inputs=[
            web_search, web_status,
            web_match_type, do_refresh
        ],
        outputs=web_output
    )

demo.launch(share=True)

# ===== Colab code cell 50 =====
# Step 1: Check the structure of your existing cricket match data

import json
from pprint import pprint

try:
    print("Total matches:", len(matches))

    if len(matches) > 0:
        print("\nFirst match details:")
        pprint(matches[0])
    else:
        print("No match data found. Run your existing backend cell first.")

except NameError:
    print("matches variable not found.")
    print("Run your existing backend/API cell first.")

# ===== Colab code cell 51 =====
import sqlite3
import json
from datetime import datetime

# Database file
DB_PATH = "/content/cricket_dashboard.db"

# Connect to SQLite database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create matches table
cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    match_id TEXT PRIMARY KEY,
    match_name TEXT NOT NULL,
    match_type TEXT,
    match_date TEXT,
    date_time_gmt TEXT,
    venue TEXT,
    status TEXT,
    match_started INTEGER DEFAULT 0,
    match_ended INTEGER DEFAULT 0,
    team1 TEXT,
    team2 TEXT,
    score_json TEXT,
    team_info_json TEXT,
    series_id TEXT,
    raw_json TEXT,
    last_saved TEXT
)
""")

# Save match data from existing matches variable
saved_count = 0

for match in matches:
    teams = match.get("teams") or []

    team1 = teams[0] if len(teams) > 0 else None
    team2 = teams[1] if len(teams) > 1 else None

    cursor.execute("""
        INSERT INTO matches (
            match_id, match_name, match_type, match_date,
            date_time_gmt, venue, status, match_started,
            match_ended, team1, team2, score_json,
            team_info_json, series_id, raw_json, last_saved
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(match_id) DO UPDATE SET
            match_name = excluded.match_name,
            match_type = excluded.match_type,
            match_date = excluded.match_date,
            date_time_gmt = excluded.date_time_gmt,
            venue = excluded.venue,
            status = excluded.status,
            match_started = excluded.match_started,
            match_ended = excluded.match_ended,
            team1 = excluded.team1,
            team2 = excluded.team2,
            score_json = excluded.score_json,
            team_info_json = excluded.team_info_json,
            series_id = excluded.series_id,
            raw_json = excluded.raw_json,
            last_saved = excluded.last_saved
    """, (
        str(match.get("id", "")),
        match.get("name"),
        match.get("matchType"),
        match.get("date"),
        match.get("dateTimeGMT"),
        match.get("venue"),
        match.get("status"),
        int(bool(match.get("matchStarted", False))),
        int(bool(match.get("matchEnded", False))),
        team1,
        team2,
        json.dumps(match.get("score", []), ensure_ascii=False),
        json.dumps(match.get("teamInfo", []), ensure_ascii=False),
        match.get("series_id"),
        json.dumps(match, ensure_ascii=False),
        datetime.now().isoformat(timespec="seconds")
    ))

    saved_count += 1

# Save changes
conn.commit()

# Verify database records
cursor.execute("SELECT COUNT(*) FROM matches")
database_count = cursor.fetchone()[0]

print("Database created successfully!")
print("Database location:", DB_PATH)
print("Matches processed:", saved_count)
print("Matches stored in database:", database_count)

# Show first five records
print("\nSample database records:")

cursor.execute("""
SELECT match_name, match_type, match_date, team1, team2, status
FROM matches
LIMIT 5
""")

for row in cursor.fetchall():
    print(row)

conn.close()

# ===== Colab code cell 52 =====
import sqlite3

# Connect to the existing database
DB_PATH = "/content/cricket_dashboard.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create players table
cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    country TEXT,
    matches_played INTEGER DEFAULT 0,
    runs INTEGER DEFAULT 0,
    wickets INTEGER DEFAULT 0,
    batting_average REAL DEFAULT 0,
    strike_rate REAL DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# Insert sample player data only if the table is empty
cursor.execute("SELECT COUNT(*) FROM players")
player_count = cursor.fetchone()[0]

if player_count == 0:
    sample_players = [
        ("Virat Kohli", "India", 10, 450, 0, 56.25, 145.0),
        ("Rohit Sharma", "India", 10, 380, 0, 42.22, 152.0),
        ("Jasprit Bumrah", "India", 8, 15, 14, 7.50, 90.0),
        ("Babar Azam", "Pakistan", 10, 390, 0, 43.33, 130.0),
        ("Shaheen Afridi", "Pakistan", 8, 12, 12, 6.00, 85.0),
        ("Steve Smith", "Australia", 9, 320, 0, 40.00, 125.0),
        ("Pat Cummins", "Australia", 8, 20, 10, 10.00, 100.0),
        ("Jos Buttler", "England", 10, 410, 0, 45.55, 150.0)
    ]

    cursor.executemany("""
        INSERT INTO players (
            player_name, country, matches_played,
            runs, wickets, batting_average, strike_rate
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, sample_players)

    conn.commit()

# Verify the players table
cursor.execute("SELECT COUNT(*) FROM players")
print("Players table created successfully!")
print("Total sample player records:", cursor.fetchone()[0])

print("\nPlayer Statistics:")
cursor.execute("""
    SELECT player_name, country, matches_played, runs, wickets
    FROM players
    ORDER BY runs DESC
""")

for row in cursor.fetchall():
    print(row)

conn.close()

# ===== Colab code cell 53 =====
import sqlite3

DB_PATH = "/content/cricket_dashboard.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=" * 50)
print("       CRICKET SQL ANALYTICS")
print("=" * 50)

# 1. Top 5 run scorers
print("\n1. TOP RUN SCORERS")
cursor.execute("""
    SELECT player_name, country, runs
    FROM players
    ORDER BY runs DESC
    LIMIT 5
""")
for row in cursor.fetchall():
    print(f"Player: {row[0]} | Country: {row[1]} | Runs: {row[2]}")

# 2. Top wicket takers
print("\n2. TOP WICKET TAKERS")
cursor.execute("""
    SELECT player_name, country, wickets
    FROM players
    ORDER BY wickets DESC
    LIMIT 5
""")
for row in cursor.fetchall():
    print(f"Player: {row[0]} | Country: {row[1]} | Wickets: {row[2]}")

# 3. Number of players by country
print("\n3. PLAYERS BY COUNTRY")
cursor.execute("""
    SELECT country, COUNT(*) AS total_players
    FROM players
    GROUP BY country
    ORDER BY total_players DESC, country
""")
for row in cursor.fetchall():
    print(f"Country: {row[0]} | Players: {row[1]}")

# 4. Match count by match type
print("\n4. MATCHES BY TYPE")
cursor.execute("""
    SELECT match_type, COUNT(*) AS total_matches
    FROM matches
    GROUP BY match_type
    ORDER BY total_matches DESC
""")
for row in cursor.fetchall():
    print(f"Match Type: {row[0]} | Matches: {row[1]}")

# 5. Total matches by completion status
print("\n5. MATCH STATUS SUMMARY")
cursor.execute("""
    SELECT
        CASE
            WHEN match_ended = 1 THEN 'Completed'
            WHEN match_started = 1 THEN 'Live/In Progress'
            ELSE 'Not Started'
        END AS status_group,
        COUNT(*) AS total_matches
    FROM matches
    GROUP BY status_group
    ORDER BY total_matches DESC
""")
for row in cursor.fetchall():
    print(f"Status: {row[0]} | Matches: {row[1]}")

conn.close()

print("\nSQL Analytics completed successfully!")

# ===== Colab code cell 54 =====
import sqlite3

DB_PATH = "/content/cricket_dashboard.db"

def create_player(name, country, matches, runs, wickets):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO players
            (player_name, country, matches_played, runs, wickets)
            VALUES (?, ?, ?, ?, ?)
        """, (name, country, matches, runs, wickets))
    print(f"Player '{name}' added successfully.")

def read_players():
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("""
            SELECT player_id, player_name, country,
                   matches_played, runs, wickets
            FROM players
            ORDER BY player_id
        """).fetchall()

    print("\nPLAYER RECORDS")
    for row in rows:
        print(row)

def update_player(player_id, new_runs):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("""
            UPDATE players
            SET runs = ?
            WHERE player_id = ?
        """, (new_runs, player_id))

    if cursor.rowcount:
        print(f"Player ID {player_id} updated successfully.")
    else:
        print(f"Player ID {player_id} not found.")

def delete_player(player_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("""
            DELETE FROM players
            WHERE player_id = ?
        """, (player_id,))

    if cursor.rowcount:
        print(f"Player ID {player_id} deleted successfully.")
    else:
        print(f"Player ID {player_id} not found.")

# Test READ operation first
read_players()

# ===== Colab code cell 55 =====
# Step 5A: Test CREATE operation

create_player(
    name="Demo Player",
    country="India",
    matches=1,
    runs=50,
    wickets=2
)

# Verify the new record
read_players()

# ===== Colab code cell 56 =====
# Step 5B: Test UPDATE operation

import sqlite3

DB_PATH = "/content/cricket_dashboard.db"

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.execute("""
        UPDATE players
        SET runs = ?
        WHERE player_name = ?
    """, (100, "Demo Player"))

    if cursor.rowcount > 0:
        print("Demo Player updated successfully!")
    else:
        print("Demo Player not found.")

# Verify the updated record
with sqlite3.connect(DB_PATH) as conn:
    result = conn.execute("""
        SELECT player_name, country, matches_played, runs, wickets
        FROM players
        WHERE player_name = ?
    """, ("Demo Player",)).fetchone()

    print("Updated record:", result)

# ===== Colab code cell 57 =====
# Step 5C: Test DELETE operation

import sqlite3

DB_PATH = "/content/cricket_dashboard.db"

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.execute("""
        DELETE FROM players
        WHERE player_name = ?
    """, ("Demo Player",))

    if cursor.rowcount > 0:
        print("Demo Player deleted successfully!")
    else:
        print("Demo Player not found.")

# Verify that Demo Player has been deleted
with sqlite3.connect(DB_PATH) as conn:
    result = conn.execute("""
        SELECT *
        FROM players
        WHERE player_name = ?
    """, ("Demo Player",)).fetchone()

    if result is None:
        print("Verification successful: Demo Player no longer exists.")
    else:
        print("Demo Player still exists:", result)

# ===== Colab code cell 58 =====
import sqlite3

DB_PATH = "/content/cricket_dashboard.db"

queries = [
    # EASY (1-10)
    ("Easy 1: Show all players",
     "SELECT * FROM players"),

    ("Easy 2: Show all match names",
     "SELECT match_name FROM matches"),

    ("Easy 3: Players from India",
     "SELECT * FROM players WHERE country = 'India'"),

    ("Easy 4: Players scoring more than 300 runs",
     "SELECT player_name, runs FROM players WHERE runs > 300"),

    ("Easy 5: Players with at least 10 wickets",
     "SELECT player_name, wickets FROM players WHERE wickets >= 10"),

    ("Easy 6: Matches of type T20",
     "SELECT match_name, match_type FROM matches WHERE LOWER(match_type) = 't20'"),

    ("Easy 7: Count total matches",
     "SELECT COUNT(*) AS total_matches FROM matches"),

    ("Easy 8: Count total players",
     "SELECT COUNT(*) AS total_players FROM players"),

    ("Easy 9: Show completed matches",
     "SELECT match_name, status FROM matches WHERE match_ended = 1"),

    ("Easy 10: Sort players by runs",
     "SELECT player_name, runs FROM players ORDER BY runs DESC"),

    # MEDIUM (11-18)
    ("Medium 11: Top 3 run scorers",
     "SELECT player_name, runs FROM players ORDER BY runs DESC LIMIT 3"),

    ("Medium 12: Top 3 wicket takers",
     "SELECT player_name, wickets FROM players ORDER BY wickets DESC LIMIT 3"),

    ("Medium 13: Player count by country",
     "SELECT country, COUNT(*) FROM players GROUP BY country"),

    ("Medium 14: Average runs per player",
     "SELECT AVG(runs) AS average_runs FROM players"),

    ("Medium 15: Highest and lowest runs",
     "SELECT MAX(runs), MIN(runs) FROM players"),

    ("Medium 16: Matches by match type",
     "SELECT match_type, COUNT(*) FROM matches GROUP BY match_type"),

    ("Medium 17: Matches at each venue",
     "SELECT venue, COUNT(*) FROM matches GROUP BY venue"),

    ("Medium 18: Players with batting average above 40",
     "SELECT player_name, batting_average FROM players WHERE batting_average > 40"),

    # HARD (19-25)
    ("Hard 19: Countries with more than one player",
     """SELECT country, COUNT(*) AS total
        FROM players GROUP BY country HAVING COUNT(*) > 1"""),

    ("Hard 20: Rank players by runs",
     """SELECT player_name, runs,
        RANK() OVER (ORDER BY runs DESC) AS run_rank
        FROM players"""),

    ("Hard 21: Percentage of each country's players",
     """SELECT country, COUNT(*) AS players,
        ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM players), 2) AS percentage
        FROM players GROUP BY country"""),

    ("Hard 22: Match status summary",
     """SELECT CASE
        WHEN match_ended = 1 THEN 'Completed'
        WHEN match_started = 1 THEN 'Live/In Progress'
        ELSE 'Not Started'
        END AS match_status, COUNT(*)
        FROM matches GROUP BY match_status"""),

    ("Hard 23: Players above overall average runs",
     """SELECT player_name, runs FROM players
        WHERE runs > (SELECT AVG(runs) FROM players)"""),

    ("Hard 24: Running total of runs",
     """SELECT player_name, runs,
        SUM(runs) OVER (ORDER BY runs DESC) AS running_total
        FROM players"""),

    ("Hard 25: Matches with team and venue information",
     """SELECT match_name, team1, team2, venue, status
        FROM matches ORDER BY match_date DESC""")
]

with sqlite3.connect(DB_PATH) as conn:
    for title, sql in queries:
        print("\n" + "=" * 60)
        print(title)
        print("-" * 60)

        try:
            cursor = conn.execute(sql)
            rows = cursor.fetchmany(10)

            if rows:
                for row in rows:
                    print(row)
            else:
                print("No records found.")

            if len(rows) == 10:
                print("Showing first 10 rows only.")

        except sqlite3.Error as error:
            print("Query error:", error)

print("\nAll 25 SQL queries have been executed.")

# ===== Colab code cell 59 =====
# Step 7: Create requirements.txt

requirements = """gradio
requests
pandas
"""

with open("/content/requirements.txt", "w") as file:
    file.write(requirements)

print("requirements.txt created successfully!")
print("\nRequired libraries:")
print(requirements)

# ===== Colab code cell 60 =====
from google.colab import files

files.download("/content/requirements.txt")

# ===== Colab code cell 61 =====
# Collect Python code from the current Google Colab notebook
# and save it into one Python file.

from google.colab import files
import json

notebook = get_ipython().user_ns.get("In", [])

# Keep code entered in notebook cells, excluding this collection cell.
current_cell = get_ipython().execution_count

all_code = []

for index, code in enumerate(notebook[1:], start=1):
    if not isinstance(code, str) or not code.strip():
        continue

    # Skip shell/magic commands and empty cells.
    if code.lstrip().startswith(("!", "%")):
        continue

    all_code.append(f"# ===== Colab code cell {index} =====\n")
    all_code.append(code.rstrip() + "\n\n")

output_path = "/content/cricket_project_code.py"

with open(output_path, "w", encoding="utf-8") as f:
    f.writelines(all_code)

print("Python code file created:", output_path)
print("Code cells collected:", len(all_code) // 2)

files.download(output_path)

# ===== Colab code cell 62 =====
import sys
import platform

print("Python Version:", sys.version)
print("Operating System:", platform.system())
print("Project Name: Cricbuzz LiveStats")
print("Environment Setup: Started")

# ===== Colab code cell 63 =====
import importlib.util

libraries = ["requests", "pandas", "streamlit", "sqlite3"]

for library in libraries:
    available = importlib.util.find_spec(library) is not None
    print(f"{library}: {'Available' if available else 'Not installed'}")

# ===== Colab code cell 64 =====
get_ipython().system('pip install streamlit')

# ===== Colab code cell 65 =====
import streamlit as st

print("Streamlit Version:", st.__version__)
print("Streamlit Installation: Successful")

# ===== Colab code cell 66 =====
import os

folders = [
    "Cricbuzz_LiveStats",
    "Cricbuzz_LiveStats/database",
    "Cricbuzz_LiveStats/sql",
    "Cricbuzz_LiveStats/pages",
    "Cricbuzz_LiveStats/utils",
    "Cricbuzz_LiveStats/docs"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print("Created:", folder)

print("\nProject folder structure created successfully!")

# ===== Colab code cell 67 =====
import sqlite3
import os

db_folder = "/content/Cricbuzz_LiveStats/database"
os.makedirs(db_folder, exist_ok=True)

db_path = os.path.join(db_folder, "cricbuzz.db")

connection = sqlite3.connect(db_path)

print("Database created successfully!")
print("Database location:", db_path)

connection.close()

# ===== Colab code cell 68 =====
import sqlite3

db_path = "/content/Cricbuzz_LiveStats/database/cricbuzz.db"

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL UNIQUE,
    country TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    team_id INTEGER,
    role TEXT,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
)
""")

cursor.execute("""
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
)
""")

cursor.execute("""
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
)
""")

connection.commit()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type = 'table'
AND name NOT LIKE 'sqlite_%'
ORDER BY name
""")

print("Tables created successfully:")
for row in cursor.fetchall():
    print("-", row[0])

connection.close()

# ===== Colab code cell 69 =====
import sqlite3

db_path = "/content/Cricbuzz_LiveStats/database/cricbuzz.db"

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Insert sample teams
cursor.executemany("""
INSERT OR IGNORE INTO teams (team_name, country)
VALUES (?, ?)
""", [
    ("India", "India"),
    ("Australia", "Australia"),
    ("England", "England")
])

# Get team IDs
cursor.execute("SELECT team_id, team_name FROM teams")
teams = {name: team_id for team_id, name in cursor.fetchall()}

# Insert sample players
cursor.executemany("""
INSERT INTO players (player_name, team_id, role)
SELECT ?, ?, ?
WHERE NOT EXISTS (
    SELECT 1 FROM players WHERE player_name = ?
)
""", [
    ("Virat Kohli", teams["India"], "Batter", "Virat Kohli"),
    ("Rohit Sharma", teams["India"], "Batter", "Rohit Sharma"),
    ("Pat Cummins", teams["Australia"], "Bowler", "Pat Cummins"),
    ("Joe Root", teams["England"], "Batter", "Joe Root")
])

connection.commit()

# Display inserted data
cursor.execute("""
SELECT p.player_name, t.team_name, p.role
FROM players p
LEFT JOIN teams t ON p.team_id = t.team_id
ORDER BY p.player_id
""")

print("Sample player data:")
for row in cursor.fetchall():
    print(row)

connection.close()

# ===== Colab code cell 70 =====
import requests
import json
from getpass import getpass

# API Key নিরাপদে ইনপুট নাও
API_KEY = getpass("Enter your Cricket API Key: ")

# Cricket API endpoint
url = "https://api.cricapi.com/v1/currentMatches"

params = {
    "apikey": API_KEY,
    "offset": 0
}

try:
    response = requests.get(url, params=params, timeout=30)

    print("HTTP Status:", response.status_code)

    data = response.json()

    # API response দেখো
    print(json.dumps(data, indent=2)[:8000])

except requests.exceptions.RequestException as e:
    print("Connection Error:", e)

except ValueError:
    print("Response JSON নয়:")
    print(response.text[:2000])

# ===== Colab code cell 71 =====
import requests
import json

# আগের API request-এর response variable যদি response হয়
data = response.json()

print("Response type:", type(data))
print("Available keys:")

if isinstance(data, dict):
    print(list(data.keys()))

print("\nResponse preview:")
print(json.dumps(data, indent=2)[:5000])

# ===== Colab code cell 72 =====
import requests
import json
from getpass import getpass

# তোমার API key নিরাপদে দাও
api_key = getpass("Enter your CricketData API key: ")

url = "https://api.cricapi.com/v1/currentMatches"

params = {
    "apikey": api_key,
    "offset": 0
}

response = requests.get(url, params=params, timeout=30)

print("HTTP Status:", response.status_code)

if response.status_code == 200:
    result = response.json()

    print("API Status:", result.get("status"))
    print("Response keys:", list(result.keys()))

    matches = result.get("data", [])

    print("Total matches:", len(matches))

    for match in matches[:10]:
        print("\nMatch:", match.get("name"))
        print("Status:", match.get("status"))
        print("Venue:", match.get("venue"))
        print("Score:", match.get("score", []))
else:
    print(response.text[:1000])

# ===== Colab code cell 73 =====
import pandas as pd

matches = result.get("data", [])

rows = []

for match in matches:
    scores = match.get("score", [])

    team_scores = []
    for score in scores:
        team = score.get("inning", "Team")
        runs = score.get("r", 0)
        wickets = score.get("w", 0)
        overs = score.get("o", 0)

        team_scores.append(
            f"{team}: {runs}/{wickets} ({overs} overs)"
        )

    rows.append({
        "Match": match.get("name", "N/A"),
        "Match Type": match.get("matchType", "N/A"),
        "Status": match.get("status", "N/A"),
        "Venue": match.get("venue", "N/A"),
        "Score": " | ".join(team_scores) or "Score unavailable"
    })

df = pd.DataFrame(rows)

display(df)

# ===== Colab code cell 74 =====
for i, match in enumerate(result.get("data", [])[:5]):
    print(f"\n--- Match {i + 1} ---")
    print("Name:", match.get("name"))
    print("Match Type:", match.get("matchType"))
    print("Series:", match.get("series"))
    print("Status:", match.get("status"))
    print("Teams:", match.get("teams"))
    print("Score:", match.get("score"))

# ===== Colab code cell 75 =====
import json

print(json.dumps(result["data"][0], indent=2))

# ===== Colab code cell 76 =====
import pandas as pd
from IPython.display import display, HTML
import html

# আগের API Cell থেকে পাওয়া result ব্যবহার করছি
matches = result.get("data", [])

def get_score(match):
    scores = match.get("score") or []
    if not scores:
        return "Score not available"

    output = []
    for s in scores:
        inning = s.get("inning", "Innings")
        runs = s.get("r", 0)
        wickets = s.get("w", 0)
        overs = s.get("o", 0)

        output.append(
            f"{inning}: {runs}/{wickets} ({overs} overs)"
        )

    return " | ".join(output)

# Match Table-এর জন্য Data তৈরি
rows = []

for match in matches:
    rows.append({
        "Match": match.get("name", "N/A"),
        "Match Type": match.get("matchType", "N/A"),
        "Status": match.get("status", "N/A"),
        "Venue": match.get("venue", "N/A"),
        "Date": match.get("date", "N/A"),
        "Score": get_score(match)
    })

df = pd.DataFrame(rows)

# Dashboard-এর Match Cards তৈরি
cards = ""

for match in matches:
    name = html.escape(str(match.get("name", "Unknown Match")))
    match_type = html.escape(str(match.get("matchType", "Cricket")))
    status = html.escape(str(match.get("status", "Status unavailable")))
    venue = html.escape(str(match.get("venue", "Venue unavailable")))
    date = html.escape(str(match.get("date", "Date unavailable")))
    score = html.escape(get_score(match))

    cards += f"""
    <div class="match-card">
        <div class="match-type">{match_type}</div>
        <h3>{name}</h3>
        <div class="score">{score}</div>
        <p><b>Status:</b> {status}</p>
        <p>📍 {venue}</p>
        <p>📅 {date}</p>
    </div>
    """

# Website-style Dashboard
dashboard = f"""
<style>
.cricket-dashboard {{
    font-family: Arial, sans-serif;
    background: #0b1220;
    color: white;
    padding: 20px;
    border-radius: 16px;
}}
.hero {{
    background: linear-gradient(120deg, #075e45, #162b53);
    padding: 25px;
    border-radius: 14px;
    margin-bottom: 20px;
}}
.hero h1 {{
    margin: 0 0 8px;
    font-size: 28px;
}}
.hero p {{
    margin: 0;
    color: #d4e6e0;
}}
.stats {{
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
}}
.stat {{
    flex: 1;
    background: #192438;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}}
.stat strong {{
    display: block;
    color: #6ee7a8;
    font-size: 26px;
}}
.match-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 14px;
}}
.match-card {{
    background: #192438;
    border: 1px solid #34445c;
    border-radius: 13px;
    padding: 16px;
    overflow-wrap: anywhere;
}}
.match-card h3 {{
    font-size: 17px;
    line-height: 1.5;
}}
.match-type {{
    color: #6ee7a8;
    font-size: 12px;
    text-transform: uppercase;
}}
.score {{
    color: #6ee7a8;
    font-weight: bold;
    line-height: 1.7;
}}
.match-card p {{
    color: #d1dbea;
    font-size: 13px;
    line-height: 1.6;
}}
</style>

<div class="cricket-dashboard">
    <div class="hero">
        <h1>🏏 Cricket Live Score</h1>
        <p>Your Cricket Dashboard</p>
    </div>

    <div class="stats">
        <div class="stat">
            <strong>{len(matches)}</strong>
            <span>Total Matches</span>
        </div>
    </div>

    <h2>Match Cards</h2>
    <div class="match-grid">
        {cards if cards else "No matches available"}
    </div>
</div>
"""

display(HTML(dashboard))

print("CRICKET MATCH TABLE")
display(df)

# ===== Colab code cell 77 =====
import requests
import pandas as pd
from IPython.display import display, HTML
from google.colab import output
import html
import json

# API key আবার নিরাপদে দাও
# আগের Cell-এ api_key variable থাকলে এই লাইনটি বাদ দিতে পারো
from getpass import getpass
if "api_key" not in globals() or not api_key:
    api_key = getpass("Enter CricketData API key: ")

def fetch_matches():
    url = "https://api.cricapi.com/v1/currentMatches"
    params = {"apikey": api_key, "offset": 0}

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "success":
        raise ValueError("API response সফল হয়নি।")

    return data.get("data", [])

def score_text(match):
    scores = match.get("score") or []
    if not scores:
        return "Score not available"

    parts = []
    for s in scores:
        parts.append(
            f"{s.get('inning', 'Innings')}: "
            f"{s.get('r', '?')}/{s.get('w', '?')} "
            f"({s.get('o', '?')} overs)"
        )
    return " | ".join(parts)

def render_dashboard(matches):
    records = []
    cards = []

    for m in matches:
        name = str(m.get("name", "Unknown match"))
        status = str(m.get("status", "Status unavailable"))
        match_type = str(m.get("matchType", "Unknown"))
        venue = str(m.get("venue", "Venue unavailable"))
        date = str(m.get("date", ""))
        score = score_text(m)

        records.append({
            "Match": name,
            "Type": match_type,
            "Status": status,
            "Venue": venue,
            "Date": date,
            "Score": score
        })

        safe = lambda value: html.escape(str(value))

        cards.append(f"""
        <article class="match-card"
          data-search="{safe(name + ' ' + status + ' ' + venue + ' ' + match_type).lower()}"
          data-status="{safe(status).lower()}">
          <span class="type">{safe(match_type)}</span>
          <h3>{safe(name)}</h3>
          <div class="score">{safe(score)}</div>
          <p>{safe(status)}</p>
          <small>📍 {safe(venue)}</small><br>
          <small>📅 {safe(date)}</small>
        </article>
        """)

    table = pd.DataFrame(records)

    page = f"""
    <style>
    .dash {{font-family:Arial,sans-serif;background:#0b1220;color:#f1f5f9;
      padding:20px;border-radius:16px}}
    .hero {{background:linear-gradient(120deg,#075e45,#172554);
      padding:22px;border-radius:13px}}
    .hero h2 {{margin:0 0 8px}}
    .tools {{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0}}
    .tools input,.tools select,.tools button {{padding:11px;border-radius:8px;
      border:1px solid #475569;font-size:14px}}
    .tools input {{flex:1;min-width:170px}}
    .tools button {{background:#16a34a;color:white;cursor:pointer}}
    .grid {{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));
      gap:13px}}
    .match-card {{background:#172337;border:1px solid #334155;
      padding:15px;border-radius:12px;overflow-wrap:anywhere}}
    .match-card h3 {{font-size:16px;line-height:1.5}}
    .type {{color:#86efac;font-size:12px;text-transform:uppercase}}
    .score {{color:#86efac;font-weight:bold;line-height:1.7}}
    .match-card p {{color:#dbeafe;line-height:1.5}}
    .match-card small {{color:#a5b4c8;line-height:1.8}}
    #count {{color:#a5f3c5;margin:12px 0}}
    </style>

    <div class="dash">
      <div class="hero">
        <h2>🏏 Cricket Live Score Dashboard</h2>
        <p>Search matches, filter results and refresh API data.</p>
      </div>

      <div class="tools">
        <input id="searchMatch" placeholder="Search team or match...">
        <select id="statusFilter">
          <option value="all">All Matches</option>
          <option value="live">Live / In Progress</option>
          <option value="completed">Completed</option>
          <option value="upcoming">Upcoming / Other</option>
        </select>
        <button onclick="filterMatches()">Search / Filter</button>
      </div>

      <div id="count">Showing {len(matches)} matches</div>
      <div class="grid" id="matchGrid">
        {''.join(cards)}
      </div>
    </div>

    <script>
    function filterMatches() {{
      const query = document.getElementById('searchMatch').value.toLowerCase();
      const filter = document.getElementById('statusFilter').value;
      const cards = document.querySelectorAll('#matchGrid .match-card');
      let visible = 0;

      cards.forEach(card => {{
        const text = card.dataset.search;
        const status = card.dataset.status;
        const isLive = /live|in progress|innings|stumps/.test(status);
        const isComplete = /won|result|complete|draw|tied/.test(status);
        let show = text.includes(query);

        if (filter === 'live') show = show && isLive;
        if (filter === 'completed') show = show && isComplete;
        if (filter === 'upcoming') show = show && !isLive && !isComplete;

        card.style.display = show ? '' : 'none';
        if (show) visible++;
      }});

      document.getElementById('count').textContent =
        'Showing ' + visible + ' matches';
    }}
    document.getElementById('searchMatch').addEventListener('input', filterMatches);
    document.getElementById('statusFilter').addEventListener('change', filterMatches);
    </script>
    """

    display(HTML(page))
    print("MATCH TABLE")
    display(table)

# Fetch fresh data, then render the dashboard and table
try:
    latest_matches = fetch_matches()
    render_dashboard(latest_matches)
except Exception as error:
    print("Dashboard refresh failed:", error)
    print("আগের API Cell এবং API key ঠিক আছে কি না পরীক্ষা করো।")

# ===== Colab code cell 78 =====
import threading
import requests
import pandas as pd
import html
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
from getpass import getpass

# 1. API Key check
if "api_key" not in globals() or not api_key:
    api_key = getpass("Enter your CricketData API key: ")

# 2. Fetch match data
def fetch_matches():
    url = "https://api.cricapi.com/v1/currentMatches"
    params = {"apikey": api_key, "offset": 0}

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "success":
        raise ValueError("API failed: " + str(data.get("info", data.get("status"))))

    return data.get("data", [])

matches = fetch_matches()

# 3. Dashboard controls
search_box = widgets.Text(
    placeholder="Search team, venue or match...",
    description="Search:",
    layout=widgets.Layout(width="70%")
)

status_filter = widgets.Dropdown(
    options=["All Matches", "Live", "Upcoming", "Completed"],
    value="All Matches",
    description="Status:"
)

refresh_button = widgets.Button(
    description="↻ Refresh Scores",
    button_style="success",
    icon="refresh"
)

dashboard_output = widgets.Output()

def safe(value):
    return html.escape(str(value if value is not None else ""))

def get_category(match):
    if match.get("matchEnded") is True:
        return "Completed"
    if match.get("matchStarted") is True:
        return "Live"
    return "Upcoming"

def get_scores(match):
    scores = match.get("score") or []
    if not scores:
        return "Score not available"

    parts = []
    for s in scores:
        team = s.get("inning", "")
        runs = s.get("r", "?")
        wickets = s.get("w", "?")
        overs = s.get("o", "?")
        parts.append(
            f"{team}: {runs}/{wickets} ({overs} overs)"
        )
    return " | ".join(parts)

# 4. Render dashboard
def render_dashboard(*args):
    query = search_box.value.strip().lower()
    selected_status = status_filter.value

    filtered = []
    for match in matches:
        category = get_category(match)
        searchable = " ".join([
            str(match.get("name", "")),
            str(match.get("venue", "")),
            str(match.get("status", "")),
            " ".join(match.get("teams") or [])
        ]).lower()

        if query and query not in searchable:
            continue
        if selected_status != "All Matches" and category != selected_status:
            continue
        filtered.append(match)

    with dashboard_output:
        clear_output(wait=True)

        live_count = sum(
            1 for m in matches if get_category(m) == "Live"
        )

        display(HTML(f"""
        <div style="background:#101827;color:white;padding:24px;
                    border-radius:16px;font-family:Arial,sans-serif;">
          <h1 style="margin:0;color:#60a5fa;">
            🏏 Cricket Live Score
          </h1>
          <p style="color:#cbd5e1;margin-bottom:20px;">
            Your Cricket Match Centre
          </p>
          <div style="display:flex;gap:12px;flex-wrap:wrap;">
            <div style="background:#1e293b;padding:16px;border-radius:12px;flex:1;min-width:110px;">
              <div style="color:#94a3b8;">Total Matches</div>
              <h2 style="margin:8px 0;">{len(matches)}</h2>
            </div>
            <div style="background:#1e293b;padding:16px;border-radius:12px;flex:1;min-width:110px;">
              <div style="color:#94a3b8;">Live Matches</div>
              <h2 style="margin:8px 0;color:#4ade80;">{live_count}</h2>
            </div>
            <div style="background:#1e293b;padding:16px;border-radius:12px;flex:1;min-width:110px;">
              <div style="color:#94a3b8;">Search Results</div>
              <h2 style="margin:8px 0;">{len(filtered)}</h2>
            </div>
          </div>
        </div>
        """))

        if not filtered:
            display(HTML("""
            <p style="padding:20px;font-family:Arial;">
              No matches found. Try another search or filter.
            </p>
            """))
            return

        cards = []
        for m in filtered:
            category = get_category(m)
            teams = m.get("teams") or []
            team_text = " vs ".join(teams) if teams else m.get("name", "Match")
            scores = get_scores(m)

            badge_color = {
                "Live": "#16a34a",
                "Upcoming": "#2563eb",
                "Completed": "#64748b"
            }.get(category, "#64748b")

            cards.append(f"""
            <div style="background:white;border:1px solid #e2e8f0;
                        border-radius:14px;padding:18px;
                        box-shadow:0 3px 10px #00000008;">
              <div style="display:flex;justify-content:space-between;
                          gap:8px;align-items:center;flex-wrap:wrap;">
                <span style="font-size:12px;color:#64748b;">
                  {safe(m.get("matchType", "Cricket"))}
                </span>
                <span style="background:{badge_color};color:white;
                             padding:5px 10px;border-radius:20px;
                             font-size:12px;">
                  {safe(category)}
                </span>
              </div>
              <h3 style="color:#0f172a;margin:16px 0 10px;">
                {safe(team_text)}
              </h3>
              <div style="background:#f1f5f9;padding:12px;
                          border-radius:8px;color:#0f172a;">
                <b>Score</b><br>{safe(scores)}
              </div>
              <p style="color:#334155;margin-bottom:5px;">
                <b>Status:</b> {safe(m.get("status", "Not available"))}
              </p>
              <p style="color:#64748b;font-size:13px;margin-bottom:5px;">
                📍 {safe(m.get("venue", "Venue not available"))}
              </p>
              <p style="color:#64748b;font-size:13px;">
                📅 {safe(m.get("date", "Date not available"))}
              </p>
            </div>
            """)

        display(HTML(f"""
        <div style="display:grid;
                    grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
                    gap:16px;margin-top:18px;">
          {''.join(cards)}
        </div>
        """))

        # Table view
        rows = []
        for m in filtered:
            rows.append({
                "Teams": " vs ".join(m.get("teams") or []),
                "Type": m.get("matchType", ""),
                "Status": get_category(m),
                "Score": get_scores(m),
                "Venue": m.get("venue", ""),
                "Date": m.get("date", "")
            })

        display(HTML("<h3 style='margin-top:24px'>Match Data Table</h3>"))
        display(pd.DataFrame(rows))

def refresh_scores(button):
    with dashboard_output:
        clear_output(wait=True)
        display(HTML("<p>Refreshing match data...</p>"))

    try:
        global matches
        matches = fetch_matches()
        render_dashboard()
    except Exception as e:
        with dashboard_output:
            clear_output(wait=True)
            display(HTML(
                "<p style='color:#dc2626'>Refresh failed: "
                + safe(e) + "</p>"
            ))

search_box.observe(render_dashboard, names="value")
status_filter.observe(render_dashboard, names="value")
refresh_button.on_click(refresh_scores)

display(widgets.HBox([search_box, status_filter, refresh_button]))
display(dashboard_output)
render_dashboard()
# Auto Refresh Settings
AUTO_REFRESH_SECONDS = 120  # 2 minutes
auto_refresh_enabled = False
auto_refresh_timer = None

def auto_refresh():
    global auto_refresh_timer

    if not auto_refresh_enabled:
        return

    try:
        global matches
        matches = fetch_matches()
        render_dashboard()
    except Exception as e:
        with dashboard_output:
            display(HTML(
                "<p style='color:#dc2626'>"
                "Auto refresh failed: " + safe(e) + "</p>"
            ))

    if auto_refresh_enabled:
        auto_refresh_timer = threading.Timer(
            AUTO_REFRESH_SECONDS, auto_refresh
        )
        auto_refresh_timer.daemon = True
        auto_refresh_timer.start()

def start_auto_refresh(button):
    global auto_refresh_enabled
    if not auto_refresh_enabled:
        auto_refresh_enabled = True
        auto_refresh()

def stop_auto_refresh(button):
    global auto_refresh_enabled, auto_refresh_timer
    auto_refresh_enabled = False

    if auto_refresh_timer is not None:
        auto_refresh_timer.cancel()

    with dashboard_output:
        display(HTML("<p>Auto Refresh stopped.</p>"))

start_button = widgets.Button(
    description="Start Auto Refresh",
    button_style="success"
)

stop_button = widgets.Button(
    description="Stop Auto Refresh",
    button_style="warning"
)

start_button.on_click(start_auto_refresh)
stop_button.on_click(stop_auto_refresh)

display(widgets.HBox([start_button, stop_button]))

# ===== Colab code cell 79 =====
# ==========================================
# Cricket Dashboard: Enhanced Features
# Auto Refresh + Last Updated + Live Highlight
# ==========================================

import threading
from datetime import datetime
from IPython.display import display, HTML
import ipywidgets as widgets

# Settings
AUTO_REFRESH_SECONDS = 120
auto_refresh_enabled = False
auto_refresh_timer = None
last_updated = "Not updated yet"

# Enhanced dashboard renderer
def render_dashboard_enhanced(*args):
    query = search_box.value.strip().lower()
    selected_status = status_filter.value

    filtered = []

    for match in matches:
        category = get_category(match)

        searchable = " ".join([
            str(match.get("name", "")),
            str(match.get("venue", "")),
            str(match.get("status", "")),
            " ".join(match.get("teams") or [])
        ]).lower()

        if query and query not in searchable:
            continue

        if selected_status != "All Matches" and category != selected_status:
            continue

        filtered.append(match)

    with dashboard_output:
        clear_output(wait=True)

        live_count = sum(
            1 for m in matches
            if get_category(m) == "Live"
        )

        display(HTML(f"""
        <div style="background:#101827;color:white;
                    padding:22px;border-radius:15px;
                    font-family:Arial,sans-serif;">
            <h1 style="color:#60a5fa;margin-top:0;">
                🏏 Cricket Live Score Dashboard
            </h1>

            <p style="color:#cbd5e1;">
                Last Updated: {safe(last_updated)}
            </p>

            <div style="display:flex;gap:12px;flex-wrap:wrap;">
                <div style="background:#1e293b;padding:14px;
                            border-radius:10px;flex:1;">
                    Total Matches
                    <h2>{len(matches)}</h2>
                </div>

                <div style="background:#1e293b;padding:14px;
                            border-radius:10px;flex:1;">
                    Live Matches
                    <h2 style="color:#4ade80;">{live_count}</h2>
                </div>

                <div style="background:#1e293b;padding:14px;
                            border-radius:10px;flex:1;">
                    Search Results
                    <h2>{len(filtered)}</h2>
                </div>
            </div>
        </div>
        """))

        if not filtered:
            display(HTML(
                "<p>No matches found. Try another search or filter.</p>"
            ))
            return

        cards = []

        for m in filtered:
            category = get_category(m)
            teams = m.get("teams") or []
            team_text = " vs ".join(teams) if teams else m.get(
                "name", "Match"
            )

            badge_color = {
                "Live": "#16a34a",
                "Upcoming": "#2563eb",
                "Completed": "#64748b"
            }.get(category, "#64748b")

            live_label = (
                '<span style="color:#dc2626;font-weight:bold;">'
                '🔴 LIVE NOW</span>'
                if category == "Live" else
                f'<span style="color:{badge_color};font-weight:bold;">'
                f'{safe(category)}</span>'
            )

            cards.append(f"""
            <div style="background:white;
                        border:1px solid #e2e8f0;
                        border-radius:14px;padding:18px;
                        box-shadow:0 3px 10px #00000010;">

                <div style="display:flex;justify-content:space-between;
                            align-items:center;gap:8px;flex-wrap:wrap;">
                    <span style="color:#64748b;font-size:12px;">
                        {safe(m.get("matchType", "Cricket"))}
                    </span>
                    {live_label}
                </div>

                <h3 style="color:#0f172a;margin-top:16px;">
                    {safe(team_text)}
                </h3>

                <div style="background:#f1f5f9;padding:13px;
                            border-radius:9px;color:#0f172a;">
                    <b>Score</b><br>
                    {safe(get_scores(m))}
                </div>

                <p style="color:#334155;">
                    <b>Status:</b>
                    {safe(m.get("status", "Not available"))}
                </p>

                <p style="color:#64748b;font-size:13px;">
                    📍 {safe(m.get("venue", "Venue not available"))}
                </p>

                <p style="color:#64748b;font-size:13px;">
                    📅 {safe(m.get("date", "Date not available"))}
                </p>
            </div>
            """)

        display(HTML(f"""
        <div style="display:grid;
                    grid-template-columns:repeat(
                        auto-fit,minmax(280px,1fr));
                    gap:16px;margin-top:18px;">
            {''.join(cards)}
        </div>
        """))

        rows = [{
            "Teams": " vs ".join(m.get("teams") or []),
            "Type": m.get("matchType", ""),
            "Status": get_category(m),
            "Score": get_scores(m),
            "Venue": m.get("venue", ""),
            "Date": m.get("date", "")
        } for m in filtered]

        display(HTML("<h3>Match Data Table</h3>"))
        display(pd.DataFrame(rows))


# Stop any previous timer
def stop_existing_timer():
    global auto_refresh_enabled, auto_refresh_timer

    auto_refresh_enabled = False

    if auto_refresh_timer is not None:
        auto_refresh_timer.cancel()
        auto_refresh_timer = None


# Auto refresh worker
def auto_refresh_worker():
    global matches, last_updated, auto_refresh_timer

    if not auto_refresh_enabled:
        return

    try:
        new_matches = fetch_matches()
        matches = new_matches
        last_updated = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        render_dashboard_enhanced()

    except Exception as e:
        with dashboard_output:
            display(HTML(
                '<p style="color:#dc2626;">'
                'Refresh failed: ' + safe(e) + '</p>'
            ))

    finally:
        if auto_refresh_enabled:
            auto_refresh_timer = threading.Timer(
                AUTO_REFRESH_SECONDS,
                auto_refresh_worker
            )
            auto_refresh_timer.daemon = True
            auto_refresh_timer.start()


# Start and stop buttons
start_auto_button = widgets.Button(
    description="Start Auto Refresh",
    button_style="success",
    icon="play"
)

stop_auto_button = widgets.Button(
    description="Stop Auto Refresh",
    button_style="warning",
    icon="stop"
)

manual_refresh_button = widgets.Button(
    description="Refresh Now",
    button_style="info",
    icon="refresh"
)


def start_auto(button):
    global auto_refresh_enabled

    if auto_refresh_enabled:
        return

    auto_refresh_enabled = True
    auto_refresh_worker()


def stop_auto(button):
    stop_existing_timer()
    render_dashboard_enhanced()


def manual_refresh(button):
    global matches, last_updated

    manual_refresh_button.disabled = True

    try:
        matches = fetch_matches()
        last_updated = datetime.now().strftime(
            "%d-%m-%Y %I:%M:%S %p"
        )
        render_dashboard_enhanced()

    except Exception as e:
        with dashboard_output:
            display(HTML(
                '<p style="color:#dc2626;">'
                'Refresh failed: ' + safe(e) + '</p>'
            ))

    finally:
        manual_refresh_button.disabled = False


# Prevent duplicate event handlers on these new buttons
start_auto_button.on_click(start_auto)
stop_auto_button.on_click(stop_auto)
manual_refresh_button.on_click(manual_refresh)

# Reuse the existing search and filter widgets
search_box.unobserve(render_dashboard, names="value")
status_filter.unobserve(render_dashboard, names="value")

search_box.observe(render_dashboard_enhanced, names="value")
status_filter.observe(render_dashboard_enhanced, names="value")

# Initial display
display(widgets.HBox([
    start_auto_button,
    stop_auto_button,
    manual_refresh_button
]))

render_dashboard_enhanced()

# ===== Colab code cell 80 =====
print("Total matches:", len(matches))

for m in matches[:10]:
    print("Match:", m.get("name"))
    print("Started:", m.get("matchStarted"))
    print("Ended:", m.get("matchEnded"))
    print("Status:", m.get("status"))
    print("-" * 40)

# ===== Colab code cell 81 =====
for m in matches[:10]:
    print("Match:", m.get("name"))
    print("Started:", m.get("matchStarted"))
    print("Ended:", m.get("matchEnded"))
    print("Status:", m.get("status"))
    print("Score:", m.get("score"))
    print("=" * 60)

# ===== Colab code cell 82 =====
def get_category(match):
    status = str(match.get("status") or "").strip().lower()

    started = match.get("matchStarted")
    ended = match.get("matchEnded")

    # Completed match detection
    completed_keywords = [
        "won by",
        "draw",
        "tied",
        "no result",
        "abandoned",
        "match drawn",
        "match tied",
        "result"
    ]

    if ended is True or any(
        keyword in status for keyword in completed_keywords
    ):
        return "Completed"

    # Live match detection
    if started is True and ended is not True:
        return "Live"

    # Upcoming match detection
    if started is False:
        return "Upcoming"

    return "Upcoming"


# Refresh dashboard using updated status detection
render_dashboard_enhanced()

# ===== Colab code cell 83 =====
print("Total matches:", len(matches))
print("Dashboard output:", dashboard_output is not None)

for m in matches[:5]:
    print("Match:", m.get("name"))
    print("Status:", m.get("status"))
    print("Category:", get_category(m))

print("Dashboard renderer exists:",
      "render_dashboard_enhanced" in globals())

# ===== Colab code cell 84 =====
render_dashboard_enhanced()

# ===== Colab code cell 85 =====
from IPython.display import display, HTML, clear_output

print("Dashboard test started")

with dashboard_output:
    clear_output(wait=True)
    display(HTML("""
        <div style="background:#101827;color:white;
                    padding:25px;border-radius:15px;">
            <h2 style="color:#60a5fa;">
                🏏 Cricket Live Score Dashboard
            </h2>
            <p>Dashboard output is working!</p>
        </div>
    """))

display(dashboard_output)

# ===== Colab code cell 86 =====
# Restore the enhanced dashboard display

try:
    print("Total matches:", len(matches))

    if "render_dashboard_enhanced" in globals():
        render_dashboard_enhanced()
        print("Enhanced dashboard function executed.")
    else:
        print("Enhanced renderer not found.")
        render_dashboard()

except Exception as e:
    print("Dashboard error:", repr(e))

# ===== Colab code cell 87 =====
from datetime import datetime

last_updated = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

print("Last Updated:", last_updated)
print("Total Matches:", len(matches))

print("\nMatch Status Summary:")

for category in ["Live", "Upcoming", "Completed"]:
    count = sum(
        1 for match in matches
        if get_category(match) == category
    )
    print(f"{category}: {count}")

# ===== Colab code cell 88 =====
# Inspect the actual API status for all matches

for i, match in enumerate(matches, start=1):
    print(f"\nMatch {i}: {match.get('name', 'Unknown')}")
    print("Status:", match.get("status", "Not available"))
    print("Started:", match.get("matchStarted"))
    print("Ended:", match.get("matchEnded"))
    print("Date:", match.get("date", "Not available"))

# ===== Colab code cell 89 =====
def get_category(match):
    status = str(match.get("status") or "").strip().lower()
    started = match.get("matchStarted")
    ended = match.get("matchEnded")

    completed_phrases = [
        "won by",
        "match tied",
        "match drawn",
        "drawn",
        "no result",
        "abandoned",
        "cancelled"
    ]

    if ended is True or any(
        phrase in status for phrase in completed_phrases
    ):
        return "Completed"

    if started is True and ended is not True:
        return "Live"

    if started is False:
        return "Upcoming"

    return "Unknown"


render_dashboard_enhanced()

# ===== Colab code cell 90 =====
print("===== CRICKET DASHBOARD CHECK =====")

print("Total Matches:", len(matches))

live_matches = [
    m for m in matches if get_category(m) == "Live"
]

completed_matches = [
    m for m in matches if get_category(m) == "Completed"
]

upcoming_matches = [
    m for m in matches if get_category(m) == "Upcoming"
]

print("Live Matches:", len(live_matches))
print("Completed Matches:", len(completed_matches))
print("Upcoming Matches:", len(upcoming_matches))

print("\n===== RECENT MATCH RESULTS =====")

for match in completed_matches[:5]:
    print("Match:", match.get("name"))
    print("Result:", match.get("status"))
    print("Date:", match.get("date"))
    print("-" * 40)

# ===== Colab code cell 91 =====
from IPython.display import display, HTML
import html

def show_recent_results():
    completed = [
        m for m in matches
        if get_category(m) == "Completed"
    ]

    cards = []

    for m in completed[:10]:
        name = html.escape(str(m.get("name") or "Match"))
        result = html.escape(
            str(m.get("status") or "Result unavailable")
        )
        date = html.escape(str(m.get("date") or "Date unavailable"))
        venue = html.escape(
            str(m.get("venue") or "Venue unavailable")
        )

        cards.append(f"""
        <div style="
            background:white;
            border:1px solid #e2e8f0;
            border-radius:14px;
            padding:18px;
            margin-bottom:14px;
            box-shadow:0 3px 10px #00000010;
        ">
            <div style="color:#64748b;font-size:12px;">
                COMPLETED MATCH
            </div>
            <h3 style="color:#0f172a;margin:10px 0;">
                🏏 {name}
            </h3>
            <p style="color:#15803d;font-weight:bold;">
                🏆 {result}
            </p>
            <p style="color:#475569;">📅 {date}</p>
            <p style="color:#64748b;">📍 {venue}</p>
        </div>
        """)

    if not cards:
        display(HTML("<p>No completed match results available.</p>"))
        return

    display(HTML(f"""
    <div style="
        background:#f8fafc;
        padding:20px;
        border-radius:16px;
        font-family:Arial,sans-serif;
    ">
        <h2 style="color:#0f172a;">
            🏆 Recent Cricket Results
        </h2>
        <p style="color:#64748b;">
            Showing the latest 10 results from the available API data.
        </p>
        {''.join(cards)}
    </div>
    """))

show_recent_results()

# ===== Colab code cell 92 =====
from IPython.display import display, HTML
import html
import pandas as pd

def show_professional_scoreboard():
    cards = []

    for match in matches:
        category = get_category(match)
        teams = match.get("teams") or []
        scores = match.get("score") or []

        team1 = html.escape(str(teams[0])) if len(teams) > 0 else "Team 1"
        team2 = html.escape(str(teams[1])) if len(teams) > 1 else "Team 2"

        score_lines = []

        for score in scores:
            inning = html.escape(str(score.get("inning", "Innings")))
            runs = score.get("r", "-")
            wickets = score.get("w", "-")
            overs = score.get("o", "-")

            score_lines.append(
                f"""
                <div style="display:flex;justify-content:space-between;
                            padding:10px 0;border-bottom:1px solid #e2e8f0;">
                    <span>{inning}</span>
                    <b>{runs}/{wickets} ({overs} overs)</b>
                </div>
                """
            )

        score_html = "".join(score_lines) if score_lines else (
            '<p style="color:#64748b;">Score not available</p>'
        )

        status = html.escape(str(match.get("status") or category))
        venue = html.escape(str(match.get("venue") or "Venue unavailable"))
        date = html.escape(str(match.get("date") or "Date unavailable"))
        match_type = html.escape(str(match.get("matchType") or "Cricket"))

        badge_colors = {
            "Live": "#16a34a",
            "Completed": "#64748b",
            "Upcoming": "#2563eb"
        }
        badge_color = badge_colors.get(category, "#64748b")

        cards.append(f"""
        <div style="background:white;border-radius:16px;
                    padding:20px;border:1px solid #e2e8f0;
                    box-shadow:0 4px 14px #0f172a10;">

            <div style="display:flex;justify-content:space-between;
                        align-items:center;gap:10px;flex-wrap:wrap;">
                <span style="color:#64748b;font-size:12px;">
                    {match_type.upper()}
                </span>
                <span style="background:{badge_color};color:white;
                             padding:5px 10px;border-radius:20px;
                             font-size:12px;">
                    {category.upper()}
                </span>
            </div>

            <div style="text-align:center;padding:18px 0;">
                <h3 style="color:#0f172a;margin:5px 0;">{team1}</h3>
                <div style="color:#94a3b8;font-weight:bold;">VS</div>
                <h3 style="color:#0f172a;margin:5px 0;">{team2}</h3>
            </div>

            <div style="background:#f8fafc;border-radius:10px;
                        padding:12px;color:#0f172a;">
                <b>INNINGS SCOREBOARD</b>
                {score_html}
            </div>

            <p style="color:#15803d;font-weight:600;margin-top:14px;">
                🏆 {status}
            </p>

            <p style="color:#64748b;font-size:13px;">
                📅 {date}
            </p>
            <p style="color:#64748b;font-size:13px;">
                📍 {venue}
            </p>
        </div>
        """)

    if not cards:
        display(HTML("<p>No match data available.</p>"))
        return

    display(HTML(f"""
    <div style="background:#f1f5f9;padding:22px;
                border-radius:18px;font-family:Arial,sans-serif;">
        <h1 style="color:#0f172a;margin-top:0;">
            🏏 Professional Cricket Scoreboard
        </h1>
        <p style="color:#64748b;">
            Total Matches: {len(matches)}
        </p>
        <div style="display:grid;
                    grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
                    gap:18px;">
            {''.join(cards)}
        </div>
    </div>
    """))

show_professional_scoreboard()

# ===== Colab code cell 93 =====
# ==========================================================
# COMPLETE CRICKET LIVE SCORE DASHBOARD
# Google Colab | CricAPI / CricketData
# ==========================================================

import requests
import pandas as pd
import html
import threading
from datetime import datetime
from getpass import getpass
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output

# ---------------- 1. CONFIGURATION ----------------

API_URL = "https://api.cricapi.com/v1/currentMatches"
AUTO_REFRESH_SECONDS = 120

if "api_key" not in globals() or not api_key:
    api_key = getpass("Enter your CricketData/CricAPI API key: ")

matches = []
last_updated = "Not updated yet"
last_error = ""
auto_refresh_enabled = False
auto_refresh_timer = None
dashboard_open = False

# ---------------- 2. FETCH MATCH DATA ----------------

def fetch_matches():
    response = requests.get(
        API_URL,
        params={"apikey": api_key, "offset": 0},
        timeout=30
    )
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "success":
        raise ValueError(
            data.get("info", "Unable to fetch match data")
        )

    return data.get("data", [])

# ---------------- 3. MATCH STATUS ----------------

def get_category(match):
    status = str(match.get("status") or "").strip().lower()
    started = match.get("matchStarted")
    ended = match.get("matchEnded")

    completed_words = [
        "won by", "match tied", "match drawn",
        "no result", "abandoned", "cancelled",
        "drawn", "innings victory"
    ]

    if ended is True or any(
        word in status for word in completed_words
    ):
        return "Completed"

    if started is True and ended is not True:
        return "Live"

    if started is False:
        return "Upcoming"

    return "Unknown"

# ---------------- 4. HELPER FUNCTIONS ----------------

def safe(value):
    return html.escape(str(value if value is not None else ""))

def get_teams(match):
    teams = match.get("teams") or []

    if isinstance(teams, list) and teams:
        return [str(team) for team in teams]

    name = str(match.get("name") or "Unknown Match")
    return [name]

def get_scores(match):
    scores = match.get("score") or []

    if not scores:
        return "Score not available"

    parts = []

    for score in scores:
        inning = score.get("inning", "Innings")
        runs = score.get("r", "-")
        wickets = score.get("w", "-")
        overs = score.get("o", "-")

        parts.append(
            f"{inning}: {runs}/{wickets} ({overs} overs)"
        )

    return " | ".join(parts)

# ---------------- 5. DASHBOARD CONTROLS ----------------

search_box = widgets.Text(
    placeholder="Search team, match or venue...",
    description="Search:",
    layout=widgets.Layout(width="100%")
)

status_filter = widgets.Dropdown(
    options=[
        "All Matches", "Live", "Upcoming",
        "Completed", "Unknown"
    ],
    value="All Matches",
    description="Status:",
    layout=widgets.Layout(width="100%")
)

refresh_button = widgets.Button(
    description="Refresh Now",
    icon="refresh",
    button_style="info"
)

start_button = widgets.Button(
    description="Start Auto Refresh",
    icon="play",
    button_style="success"
)

stop_button = widgets.Button(
    description="Stop Auto Refresh",
    icon="stop",
    button_style="warning",
    disabled=True
)

dashboard_output = widgets.Output()

# ---------------- 6. RENDER DASHBOARD ----------------

def render_dashboard(*args):
    query = search_box.value.strip().lower()
    selected = status_filter.value

    filtered = []

    for match in matches:
        category = get_category(match)
        teams = get_teams(match)

        searchable = " ".join([
            str(match.get("name", "")),
            str(match.get("venue", "")),
            str(match.get("status", "")),
            " ".join(teams)
        ]).lower()

        if query and query not in searchable:
            continue

        if selected != "All Matches" and category != selected:
            continue

        filtered.append(match)

    live_count = sum(
        1 for m in matches if get_category(m) == "Live"
    )
    completed_count = sum(
        1 for m in matches if get_category(m) == "Completed"
    )
    upcoming_count = sum(
        1 for m in matches if get_category(m) == "Upcoming"
    )

    cards = []

    for match in filtered:
        teams = get_teams(match)
        category = get_category(match)

        team1 = safe(teams[0])
        team2 = safe(teams[1]) if len(teams) > 1 else ""

        if len(teams) > 2:
            team1 = safe(" vs ".join(teams))

        if team2:
            matchup = f"{team1} <span style='color:#94a3b8'>VS</span> {team2}"
        else:
            matchup = team1

        colors = {
            "Live": "#16a34a",
            "Upcoming": "#2563eb",
            "Completed": "#64748b",
            "Unknown": "#64748b"
        }
        color = colors.get(category, "#64748b")

        score_html = safe(get_scores(match))
        result = safe(match.get("status") or "Status unavailable")
        venue = safe(match.get("venue") or "Venue unavailable")
        date = safe(match.get("date") or "Date unavailable")
        match_type = safe(match.get("matchType") or "Cricket")

        live_label = (
            "🔴 LIVE NOW"
            if category == "Live"
            else category.upper()
        )

        cards.append(f"""
        <div style="
            background:white;
            border:1px solid #e2e8f0;
            border-radius:15px;
            padding:18px;
            box-shadow:0 4px 12px #0000000c;
            min-width:0;
        ">
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                gap:8px;
                flex-wrap:wrap;
            ">
                <span style="color:#64748b;font-size:12px">
                    {match_type.upper()}
                </span>
                <span style="
                    background:{color};
                    color:white;
                    border-radius:20px;
                    padding:5px 9px;
                    font-size:11px;
                    font-weight:bold;
                ">{live_label}</span>
            </div>

            <h3 style="
                text-align:center;
                color:#0f172a;
                margin:20px 0;
                line-height:1.6;
            ">{matchup}</h3>

            <div style="
                background:#f1f5f9;
                color:#0f172a;
                padding:13px;
                border-radius:9px;
                overflow-wrap:anywhere;
            ">
                <b>🏏 SCOREBOARD</b>
                <div style="margin-top:10px;line-height:1.8">
                    {score_html}
                </div>
            </div>

            <p style="color:#15803d;font-weight:600">
                🏆 {result}
            </p>
            <p style="color:#64748b;font-size:13px">
                📅 {date}
            </p>
            <p style="color:#64748b;font-size:13px">
                📍 {venue}
            </p>
        </div>
        """)

    rows = []

    for match in filtered:
        rows.append({
            "Teams": " vs ".join(get_teams(match)),
            "Type": match.get("matchType", ""),
            "Category": get_category(match),
            "Score": get_scores(match),
            "Result / Status": match.get("status", ""),
            "Venue": match.get("venue", ""),
            "Date": match.get("date", "")
        })

    with dashboard_output:
        clear_output(wait=True)

        display(HTML(f"""
        <div style="
            background:#101827;
            color:white;
            padding:24px;
            border-radius:16px;
            font-family:Arial,sans-serif;
        ">
            <h1 style="color:#60a5fa;margin:0">
                🏏 Cricket Live Score
            </h1>
            <p style="color:#cbd5e1">
                Your Complete Cricket Match Centre
            </p>
            <p style="color:#cbd5e1;font-size:13px">
                Last successful update: {safe(last_updated)}
            </p>
            <div style="
                display:grid;
                grid-template-columns:repeat(auto-fit,minmax(120px,1fr));
                gap:10px;
                margin-top:20px;
            ">
                <div style="background:#1e293b;padding:14px;border-radius:10px">
                    <div style="color:#cbd5e1">Total Matches</div>
                    <h2>{len(matches)}</h2>
                </div>
                <div style="background:#1e293b;padding:14px;border-radius:10px">
                    <div style="color:#86efac">Live</div>
                    <h2>{live_count}</h2>
                </div>
                <div style="background:#1e293b;padding:14px;border-radius:10px">
                    <div style="color:#93c5fd">Upcoming</div>
                    <h2>{upcoming_count}</h2>
                </div>
                <div style="background:#1e293b;padding:14px;border-radius:10px">
                    <div style="color:#cbd5e1">Completed</div>
                    <h2>{completed_count}</h2>
                </div>
            </div>
        </div>
        """))

        if last_error:
            display(HTML(f"""
            <div style="background:#fef2f2;color:#991b1b;
                        padding:12px;margin-top:12px;border-radius:8px">
                <b>Refresh warning:</b> {safe(last_error)}
            </div>
            """))

        display(HTML(
            "<h2 style='font-family:Arial;color:#0f172a;"
            "margin-top:24px'>🏆 Match Scoreboards</h2>"
        ))

        if cards:
            display(HTML(f"""
            <div style="
                display:grid;
                grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
                gap:16px;
                font-family:Arial,sans-serif;
            ">
                {''.join(cards)}
            </div>
            """))
        else:
            display(HTML("""
            <p style="padding:15px;color:#64748b">
                No matches found. Try another search or filter.
            </p>
            """))

        display(HTML(
            "<h2 style='font-family:Arial;color:#0f172a;"
            "margin-top:28px'>📋 Match Data Table</h2>"
        ))

        if rows:
            display(pd.DataFrame(rows).reset_index(drop=True))
        else:
            display(HTML("<p>No table data available.</p>"))

        display(HTML("""
        <p style="color:#64748b;font-size:12px;margin-top:16px">
            Scores and results are provided by the connected API.
            Live updates depend on API data availability.
        </p>
        """))

# ---------------- 7. REFRESH FUNCTIONS ----------------

def refresh_data():
    global matches, last_updated, last_error

    new_matches = fetch_matches()
    matches = new_matches
    last_updated = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    last_error = ""

def on_refresh(button):
    refresh_button.disabled = True

    try:
        refresh_data()
    except Exception as error:
        global last_error
        last_error = str(error)

    render_dashboard()
    refresh_button.disabled = False

# ---------------- 8. AUTO REFRESH ----------------

def auto_refresh_worker():
    global auto_refresh_timer, last_error

    if not auto_refresh_enabled:
        return

    try:
        refresh_data()
    except Exception as error:
        last_error = str(error)

    render_dashboard()

    if auto_refresh_enabled:
        auto_refresh_timer = threading.Timer(
            AUTO_REFRESH_SECONDS,
            auto_refresh_worker
        )
        auto_refresh_timer.daemon = True
        auto_refresh_timer.start()

def on_start(button):
    global auto_refresh_enabled

    if auto_refresh_enabled:
        return

    auto_refresh_enabled = True
    start_button.disabled = True
    stop_button.disabled = False

    # First refresh happens immediately.
    auto_refresh_worker()

def on_stop(button):
    global auto_refresh_enabled, auto_refresh_timer

    auto_refresh_enabled = False

    if auto_refresh_timer is not None:
        auto_refresh_timer.cancel()
        auto_refresh_timer = None

    start_button.disabled = False
    stop_button.disabled = True
    render_dashboard()

# ---------------- 9. CONNECT CONTROLS ----------------

search_box.observe(render_dashboard, names="value")
status_filter.observe(render_dashboard, names="value")

refresh_button.on_click(on_refresh)
start_button.on_click(on_start)
stop_button.on_click(on_stop)

# ---------------- 10. INITIALIZE DASHBOARD ----------------

controls = widgets.VBox([
    search_box,
    status_filter,
    widgets.HBox([
        refresh_button,
        start_button,
        stop_button
    ])
])

display(HTML("""
<div style="font-family:Arial,sans-serif;padding:10px 0">
<h2>🏏 Complete Cricket Dashboard</h2>
<p>Search matches, filter results and refresh scores.</p>
</div>
"""))

display(controls)
display(dashboard_output)

try:
    refresh_data()
except Exception as error:
    last_error = str(error)
    print("API Error:", last_error)

render_dashboard()

print("Dashboard initialized.")

# ===== Colab code cell 94 =====
# ============================================================
# CRICKET LIVE SCORE DASHBOARD - ADVANCED COLAB VERSION
# Features: Live Score Cards, Search, Filters, Auto Refresh
# ============================================================

import requests
import pandas as pd
import html
import time
import threading
from datetime import datetime
from getpass import getpass
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output

# 1. API setup
API_URL = "https://api.cricapi.com/v1/currentMatches"

if "api_key" not in globals() or not api_key:
    api_key = getpass("Enter your Cricket API key: ")

matches = []
last_updated = "Not updated yet"
last_error = ""
auto_refresh_enabled = False
auto_refresh_thread = None
refresh_lock = threading.Lock()
auto_refresh_stop = threading.Event()


def safe(value):
    """Safely display text in HTML."""
    if value is None or value == "":
        return "N/A"
    return html.escape(str(value))


# 2. Match status detection
def get_category(match):
    status = str(match.get("status", "")).lower()
    started = match.get("matchStarted", False)
    ended = match.get("matchEnded", False)

    if ended or any(word in status for word in [
        "won by", "draw", "tied", "no result", "abandoned"
    ]):
        return "Completed"

    if started or any(word in status for word in [
        "live", "in progress", "innings break", "stumps",
        "day ", "need ", "trail by"
    ]):
        return "Live"

    return "Upcoming"


# 3. Team names and scores
def get_teams(match):
    teams = match.get("teams") or []
    if isinstance(teams, list) and teams:
        return [str(t) for t in teams]
    return ["Team 1", "Team 2"]


def get_scores(match):
    score_list = match.get("score") or []
    if not isinstance(score_list, list) or not score_list:
        return "Score not available"

    result = []
    for item in score_list:
        if not isinstance(item, dict):
            continue

        inning = item.get("inning", "")
        runs = item.get("r", "?")
        wickets = item.get("w", "?")
        overs = item.get("o", "?")

        result.append(
            f"{inning}: {runs}/{wickets} ({overs} overs)"
            if inning else f"{runs}/{wickets} ({overs} overs)"
        )

    return " | ".join(result) if result else "Score not available"


# 4. Fetch the latest matches
def fetch_matches():
    response = requests.get(
        API_URL,
        params={"apikey": api_key, "offset": 0},
        timeout=25
    )
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "success":
        raise RuntimeError(
            data.get("reason", "API did not return success.")
        )

    result = data.get("data", [])
    if not isinstance(result, list):
        raise RuntimeError("Unexpected match data format.")

    return result


# 5. Dashboard controls
search_box = widgets.Text(
    placeholder="Search team, venue or match...",
    description="Search:",
    layout=widgets.Layout(width="55%")
)

status_filter = widgets.Dropdown(
    options=["All", "Live", "Upcoming", "Completed"],
    value="All",
    description="Status:"
)

type_filter = widgets.Dropdown(
    options=["All"],
    value="All",
    description="Match type:"
)

refresh_button = widgets.Button(
    description="Refresh Scores",
    button_style="primary",
    icon="refresh"
)

start_button = widgets.Button(
    description="Start Auto Refresh",
    button_style="success",
    icon="play"
)

stop_button = widgets.Button(
    description="Stop Auto Refresh",
    button_style="warning",
    icon="stop",
    disabled=True
)

interval_dropdown = widgets.Dropdown(
    options=[
        ("30 seconds", 30),
        ("60 seconds", 60),
        ("120 seconds", 120),
        ("5 minutes", 300)
    ],
    value=120,
    description="Interval:"
)

summary_output = widgets.Output()
cards_output = widgets.Output()
table_output = widgets.Output()
message_output = widgets.Output()


# 6. Filter matches
def get_filtered_matches():
    query = search_box.value.strip().lower()
    chosen_status = status_filter.value
    chosen_type = type_filter.value

    filtered = []

    for match in matches:
        teams = get_teams(match)
        category = get_category(match)
        match_type = str(match.get("matchType", "Unknown")).upper()

        searchable = " ".join([
            str(match.get("name", "")),
            str(match.get("venue", "")),
            str(match.get("status", "")),
            " ".join(teams),
            match_type
        ]).lower()

        if query and query not in searchable:
            continue
        if chosen_status != "All" and category != chosen_status:
            continue
        if chosen_type != "All" and match_type != chosen_type:
            continue

        filtered.append(match)

    return filtered


# 7. Professional dashboard rendering
def render_dashboard():
    filtered = get_filtered_matches()

    with summary_output:
        clear_output(wait=True)
        counts = {
            category: sum(
                1 for m in matches if get_category(m) == category
            )
            for category in ["Live", "Upcoming", "Completed"]
        }

        display(HTML(f"""
        <div style="display:flex;flex-wrap:wrap;gap:12px;margin:12px 0;">
          <div style="background:#172554;color:white;padding:18px;border-radius:12px;min-width:125px;">
            <div>Total Matches</div>
            <div style="font-size:28px;font-weight:bold;">{len(matches)}</div>
          </div>
          <div style="background:#166534;color:white;padding:18px;border-radius:12px;min-width:125px;">
            <div>Live</div>
            <div style="font-size:28px;font-weight:bold;">{counts["Live"]}</div>
          </div>
          <div style="background:#92400e;color:white;padding:18px;border-radius:12px;min-width:125px;">
            <div>Upcoming</div>
            <div style="font-size:28px;font-weight:bold;">{counts["Upcoming"]}</div>
          </div>
          <div style="background:#374151;color:white;padding:18px;border-radius:12px;min-width:125px;">
            <div>Completed</div>
            <div style="font-size:28px;font-weight:bold;">{counts["Completed"]}</div>
          </div>
        </div>
        <div style="color:#64748b;font-size:13px;">
          Last successful update: {safe(last_updated)}
        </div>
        """))

    with cards_output:
        clear_output(wait=True)

        if not filtered:
            display(HTML(
                "<p style='padding:16px;'>No matches found for these filters.</p>"
            ))
        else:
            card_html = ""

            for match in filtered:
                category = get_category(match)
                teams = get_teams(match)
                team_text = " vs ".join(teams)
                match_type = str(match.get("matchType", "Unknown")).upper()
                score_text = get_scores(match)
                status_text = match.get("status", "Status unavailable")
                venue = match.get("venue", "Venue unavailable")
                date = match.get("date", "Date unavailable")

                badge_color = {
                    "Live": "#b91c1c",
                    "Upcoming": "#a16207",
                    "Completed": "#166534"
                }.get(category, "#475569")

                card_html += f"""
                <div style="
                    background:#ffffff;color:#111827;
                    border:1px solid #e5e7eb;border-radius:14px;
                    padding:18px;margin:12px 0;
                    box-shadow:0 3px 10px rgba(0,0,0,.06);
                ">
                  <div style="display:flex;justify-content:space-between;
                              flex-wrap:wrap;gap:8px;">
                    <b>{safe(match_type)} · {safe(match.get("name", team_text))}</b>
                    <span style="background:{badge_color};color:white;
                                 padding:4px 10px;border-radius:20px;font-size:12px;">
                      {safe(category)}
                    </span>
                  </div>
                  <h3 style="margin:14px 0 8px;">{safe(team_text)}</h3>
                  <div style="font-size:15px;font-weight:600;margin-bottom:10px;">
                    {safe(score_text)}
                  </div>
                  <div style="color:#475569;margin:6px 0;">
                    {safe(status_text)}
                  </div>
                  <div style="color:#64748b;font-size:13px;">
                    Venue: {safe(venue)} · Date: {safe(date)}
                  </div>
                </div>
                """

            display(HTML(card_html))

    with table_output:
        clear_output(wait=True)

        rows = []
        for match in filtered:
            rows.append({
                "Match": match.get("name", "Unknown"),
                "Type": match.get("matchType", "Unknown"),
                "Category": get_category(match),
                "Status / Result": match.get("status", "N/A"),
                "Score": get_scores(match),
                "Venue": match.get("venue", "N/A"),
                "Date": match.get("date", "N/A")
            })

        if rows:
            display(pd.DataFrame(rows))
        else:
            print("No data to display.")


# 8. Refresh function
def refresh_data(_=None):
    global matches, last_updated, last_error

    if not refresh_lock.acquire(blocking=False):
        return

    try:
        new_matches = fetch_matches()
        matches = new_matches
        last_updated = datetime.now().strftime("%d %b %Y, %I:%M:%S %p")
        last_error = ""

        available_types = sorted({
            str(m.get("matchType", "Unknown")).upper()
            for m in matches
        })

        current_type = type_filter.value
        type_filter.options = ["All"] + available_types
        type_filter.value = (
            current_type if current_type in available_types else "All"
        )

        with message_output:
            clear_output(wait=True)
            print(f"Updated successfully. {len(matches)} matches loaded.")

    except Exception as exc:
        last_error = str(exc)
        with message_output:
            clear_output(wait=True)
            print("Refresh failed:", last_error)
            print("Check your API key, API plan and internet connection.")

    finally:
        refresh_lock.release()

    render_dashboard()


# 9. Auto-refresh controls
def auto_refresh_worker():
    global auto_refresh_enabled

    while not auto_refresh_stop.is_set():
        wait_seconds = interval_dropdown.value

        if auto_refresh_stop.wait(wait_seconds):
            break

        if auto_refresh_enabled:
            refresh_data()

    auto_refresh_enabled = False
    start_button.disabled = False
    stop_button.disabled = True


def start_auto_refresh(_):
    global auto_refresh_enabled, auto_refresh_thread

    if auto_refresh_enabled:
        return

    auto_refresh_stop.clear()
    auto_refresh_enabled = True
    start_button.disabled = True
    stop_button.disabled = False

    auto_refresh_thread = threading.Thread(
        target=auto_refresh_worker,
        daemon=True
    )
    auto_refresh_thread.start()

    with message_output:
        clear_output(wait=True)
        print(f"Auto refresh started: every {interval_dropdown.value} seconds.")


def stop_auto_refresh(_):
    global auto_refresh_enabled

    auto_refresh_enabled = False
    auto_refresh_stop.set()
    start_button.disabled = False
    stop_button.disabled = True

    with message_output:
        clear_output(wait=True)
        print("Auto refresh stopped.")


refresh_button.on_click(refresh_data)
start_button.on_click(start_auto_refresh)
stop_button.on_click(stop_auto_refresh)

search_box.observe(lambda change: render_dashboard(), names="value")
status_filter.observe(lambda change: render_dashboard(), names="value")
type_filter.observe(lambda change: render_dashboard(), names="value")


# 10. Display the complete dashboard
display(HTML("""
<div style="background:#0f172a;color:white;padding:24px;border-radius:16px;">
  <h1 style="margin:0;">🏏 Cricket Live Score Dashboard</h1>
  <p style="margin-bottom:0;">Scores · Match Status · Search · Auto Refresh</p>
</div>
"""))

display(widgets.HBox([search_box]))
display(widgets.HBox([status_filter, type_filter]))
display(widgets.HBox([refresh_button, interval_dropdown]))
display(widgets.HBox([start_button, stop_button]))
display(message_output)
display(summary_output)

display(HTML("<h3>Match Scoreboard</h3>"))
display(cards_output)

display(HTML("<h3>Match Data Table</h3>"))
display(table_output)

refresh_data()

# ===== Colab code cell 95 =====
# ============================================================
# CRICKET DASHBOARD WEB APP - GRADIO
# Run this cell after Step 1
# ============================================================

get_ipython().run_line_magic('pip', '-q install gradio')

import gradio as gr
from datetime import datetime
import html


def make_web_dashboard(search, status, match_type, refresh_now):
    global matches, last_updated

    # Fetch fresh data when Refresh is clicked
    if refresh_now:
        try:
            matches = fetch_matches()
            last_updated = datetime.now().strftime("%d %b %Y, %I:%M:%S %p")
        except Exception as exc:
            return (
                f"<h3>Could not refresh scores</h3>"
                f"<p>{html.escape(str(exc))}</p>"
            )

    query = (search or "").strip().lower()
    results = []

    for match in matches:
        teams = get_teams(match)
        category = get_category(match)
        mtype = str(match.get("matchType", "Unknown")).upper()

        searchable = " ".join([
            str(match.get("name", "")),
            str(match.get("venue", "")),
            str(match.get("status", "")),
            " ".join(teams),
            mtype
        ]).lower()

        if query and query not in searchable:
            continue
        if status != "All" and category != status:
            continue
        if match_type != "All" and mtype != match_type:
            continue

        results.append(match)

    counts = {
        c: sum(1 for m in matches if get_category(m) == c)
        for c in ["Live", "Upcoming", "Completed"]
    }

    page = f"""
    <div style="font-family:Arial,sans-serif;color:#111827;">
      <div style="background:#0f172a;color:white;padding:24px;
                  border-radius:16px;margin-bottom:16px;">
        <h1 style="margin:0;">🏏 Cricket Live Score</h1>
        <p>Match Centre · Search · Filters</p>
        <small>Last update: {html.escape(str(last_updated))}</small>
      </div>

      <div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:20px;">
        <div style="background:#172554;color:white;padding:16px;border-radius:12px;">
          Total Matches: <b>{len(matches)}</b>
        </div>
        <div style="background:#166534;color:white;padding:16px;border-radius:12px;">
          Live: <b>{counts["Live"]}</b>
        </div>
        <div style="background:#92400e;color:white;padding:16px;border-radius:12px;">
          Upcoming: <b>{counts["Upcoming"]}</b>
        </div>
        <div style="background:#374151;color:white;padding:16px;border-radius:12px;">
          Completed: <b>{counts["Completed"]}</b>
        </div>
      </div>
    """

    if not results:
        page += "<p>No matches found. Try changing your search or filters.</p>"

    for match in results:
        category = get_category(match)
        badge_color = {
            "Live": "#b91c1c",
            "Upcoming": "#a16207",
            "Completed": "#166534"
        }.get(category, "#475569")

        page += f"""
        <div style="border:1px solid #e5e7eb;border-radius:14px;
                    padding:18px;margin:12px 0;background:white;">
          <div style="display:flex;justify-content:space-between;
                      gap:10px;flex-wrap:wrap;">
            <b>{html.escape(str(match.get("matchType", "Unknown")).upper())}
            · {html.escape(str(match.get("name", "Cricket Match")))}</b>
            <span style="background:{badge_color};color:white;
                         padding:4px 10px;border-radius:20px;">
              {category}
            </span>
          </div>
          <h3>{html.escape(" vs ".join(get_teams(match)))}</h3>
          <p><b>{html.escape(get_scores(match))}</b></p>
          <p>{html.escape(str(match.get("status", "Status unavailable")))}</p>
          <small>
            Venue: {html.escape(str(match.get("venue", "N/A")))}
            · Date: {html.escape(str(match.get("date", "N/A")))}
          </small>
        </div>
        """

    page += "</div>"
    return page


with gr.Blocks(title="Cricket Live Score Dashboard") as demo:
    gr.Markdown("# 🏏 Cricket Live Score Dashboard")
    gr.Markdown("Search matches, apply filters and refresh the score feed.")

    with gr.Row():
        web_search = gr.Textbox(
            label="Search",
            placeholder="Team, venue or match name"
        )
        web_status = gr.Dropdown(
            ["All", "Live", "Upcoming", "Completed"],
            value="All",
            label="Match Status"
        )

    web_types = sorted({
        str(m.get("matchType", "Unknown")).upper()
        for m in matches
    })
    web_match_type = gr.Dropdown(
        ["All"] + web_types,
        value="All",
        label="Match Type"
    )

    web_refresh = gr.Button("🔄 Refresh Scores", variant="primary")
    web_output = gr.HTML()

    # Update display when filters change
    web_search.change(
        make_web_dashboard,
        [web_search, web_status, web_match_type, gr.State(False)],
        web_output
    )
    web_status.change(
        make_web_dashboard,
        [web_search, web_status, web_match_type, gr.State(False)],
        web_output
    )
    web_match_type.change(
        make_web_dashboard,
        [web_search, web_status, web_match_type, gr.State(False)],
        web_output
    )
    web_refresh.click(
        make_web_dashboard,
        [web_search, web_status, web_match_type, gr.State(True)],
        web_output
    )

    demo.load(
        make_web_dashboard,
        [web_search, web_status, web_match_type, gr.State(False)],
        web_output
    )
    # Auto-refresh every 120 seconds
    web_timer = gr.Timer(value=120, active=True)

    web_timer.tick(
        fn=make_web_dashboard,
        inputs=[
            web_search,
            web_status,
            web_match_type,
            gr.State(True)
        ],
        outputs=[web_output]
    )

demo.launch(share=True)

# ===== Colab code cell 96 =====
# ============================================================
# CRICKET LIVE SCORE DASHBOARD - PROFESSIONAL WEB APP
# Google Colab + Gradio
# Keeps existing backend, search, filters and auto-refresh
# ============================================================

get_ipython().run_line_magic('pip', '-q install gradio')

import gradio as gr
from datetime import datetime
import html

# Keep existing backend functions:
# fetch_matches(), get_teams(), get_category(), get_scores()
# Existing global variables: matches, last_updated


def make_web_dashboard(search, status, match_type, refresh_now):
    global matches, last_updated

    # Fetch fresh scores when requested by button or timer
    if refresh_now:
        try:
            matches = fetch_matches()
            last_updated = datetime.now().strftime(
                "%d %b %Y, %I:%M:%S %p"
            )
        except Exception as exc:
            error_message = html.escape(str(exc))
            return f"""
            <div style="background:#fff1f2;color:#9f1239;
                        padding:24px;border-radius:16px;
                        font-family:Arial,sans-serif;">
                <h2>Unable to refresh scores</h2>
                <p>{error_message}</p>
                <p>Please check your API connection.</p>
            </div>
            """

    query = (search or "").strip().lower()
    results = []

    # Search and filters: preserved
    for match in matches:
        teams = get_teams(match)
        category = get_category(match)
        mtype = str(match.get("matchType", "Unknown")).upper()

        searchable = " ".join([
            str(match.get("name", "")),
            str(match.get("venue", "")),
            str(match.get("status", "")),
            " ".join(teams),
            mtype
        ]).lower()

        if query and query not in searchable:
            continue

        if status != "All" and category != status:
            continue

        if match_type != "All" and mtype != match_type:
            continue

        results.append(match)

    counts = {
        category: sum(
            1 for match in matches
            if get_category(match) == category
        )
        for category in ["Live", "Upcoming", "Completed"]
    }

    # Professional responsive design
    page = """
    <style>
      .cricket-app {
        font-family: Inter, Arial, sans-serif;
        color: #e5e7eb;
        background: #080f1e;
        padding: 18px;
        border-radius: 20px;
      }
      .cricket-hero {
        background: linear-gradient(120deg,#102b4e,#164e63);
        border: 1px solid #24516d;
        border-radius: 18px;
        padding: 26px;
        margin-bottom: 18px;
      }
      .cricket-hero h1 {
        font-size: clamp(25px,4vw,36px);
        margin: 0 0 8px;
        color: white;
      }
      .cricket-muted { color: #a8bfd3; }
      .cricket-stats {
        display: grid;
        grid-template-columns: repeat(4,minmax(0,1fr));
        gap: 12px;
        margin-bottom: 22px;
      }
      .cricket-stat {
        background: #111c30;
        border: 1px solid #25344b;
        border-radius: 14px;
        padding: 17px;
      }
      .cricket-stat-label {
        color: #a8b6ca;
        font-size: 13px;
      }
      .cricket-stat-value {
        font-size: 27px;
        font-weight: 750;
        margin-top: 8px;
        color: white;
      }
      .cricket-section-title {
        font-size: 20px;
        font-weight: 700;
        margin: 22px 0 12px;
        color: white;
      }
      .cricket-match {
        background: #111c30;
        border: 1px solid #293950;
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
        overflow-wrap: anywhere;
      }
      .cricket-match-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
      }
      .cricket-match-name {
        font-weight: 700;
        color: #f3f7ff;
        font-size: 15px;
      }
      .cricket-badge {
        border-radius: 999px;
        padding: 6px 11px;
        font-size: 12px;
        font-weight: 700;
      }
      .cricket-teams {
        font-size: 21px;
        font-weight: 750;
        color: white;
        margin: 20px 0 10px;
      }
      .cricket-score {
        background: #0b1425;
        border-radius: 10px;
        padding: 13px;
        font-size: 18px;
        font-weight: 700;
        color: #93c5fd;
      }
      .cricket-status {
        color: #d2dbea;
        line-height: 1.6;
        margin: 12px 0;
      }
      .cricket-meta {
        color: #9eafc5;
        font-size: 12px;
        line-height: 1.8;
      }
      .cricket-empty {
        padding: 28px;
        text-align: center;
        border: 1px dashed #475569;
        border-radius: 14px;
        color: #cbd5e1;
      }
      @media(max-width:600px) {
        .cricket-app { padding: 10px; }
        .cricket-hero { padding: 19px; }
        .cricket-stats { grid-template-columns: repeat(2,minmax(0,1fr)); }
        .cricket-stat { padding: 13px; }
        .cricket-stat-value { font-size: 23px; }
        .cricket-match { padding: 15px; }
        .cricket-teams { font-size: 18px; }
      }
    </style>
    <div class="cricket-app">
      <div class="cricket-hero">
        <div style="font-size:12px;letter-spacing:2px;
                    color:#a5e6d0;font-weight:700;">
          LIVE CRICKET · MATCH CENTRE
        </div>
        <h1>🏏 Cricket Live Score</h1>
        <p class="cricket-muted">
          Your cricket dashboard for match scores and updates.
        </p>
    """

    page += f"""
        <div class="cricket-muted" style="font-size:12px;">
          Last data refresh: {html.escape(str(last_updated))}
        </div>
      </div>

      <div class="cricket-stats">
        <div class="cricket-stat">
          <div class="cricket-stat-label">TOTAL MATCHES</div>
          <div class="cricket-stat-value">{len(matches)}</div>
        </div>
        <div class="cricket-stat">
          <div class="cricket-stat-label">🔴 LIVE</div>
          <div class="cricket-stat-value" style="color:#f87171;">
            {counts["Live"]}
          </div>
        </div>
        <div class="cricket-stat">
          <div class="cricket-stat-label">📅 UPCOMING</div>
          <div class="cricket-stat-value" style="color:#fbbf24;">
            {counts["Upcoming"]}
          </div>
        </div>
        <div class="cricket-stat">
          <div class="cricket-stat-label">✓ COMPLETED</div>
          <div class="cricket-stat-value" style="color:#6ee7b7;">
            {counts["Completed"]}
          </div>
        </div>
      </div>

      <div class="cricket-section-title">
        Match Centre
        <span style="font-size:13px;color:#9eafc5;font-weight:400;">
          · {len(results)} result(s)
        </span>
      </div>
    """

    if not results:
        page += """
        <div class="cricket-empty">
          <div style="font-size:30px;">🏏</div>
          <h3>No matches found</h3>
          <p>Try another search term or change your filters.</p>
        </div>
        """

    for match in results:
        category = get_category(match)
        teams = " vs ".join(get_teams(match))
        mtype = str(match.get("matchType", "Unknown")).upper()

        badge_colors = {
            "Live": ("#451a1a", "#fca5a5"),
            "Upcoming": ("#422006", "#fcd34d"),
            "Completed": ("#064e3b", "#6ee7b7")
        }
        bg, fg = badge_colors.get(
            category, ("#25344b", "#cbd5e1")
        )

        page += f"""
        <div class="cricket-match">
          <div class="cricket-match-top">
            <div class="cricket-match-name">
              {html.escape(mtype)} ·
              {html.escape(str(match.get("name", "Cricket Match")))}
            </div>
            <span class="cricket-badge"
                  style="background:{bg};color:{fg};">
              {html.escape(str(category))}
            </span>
          </div>

          <div class="cricket-teams">
            {html.escape(teams)}
          </div>

          <div class="cricket-score">
            {html.escape(str(get_scores(match)))}
          </div>

          <div class="cricket-status">
            {html.escape(str(match.get("status", "Status unavailable")))}
          </div>

          <div class="cricket-meta">
            📍 Venue: {html.escape(str(match.get("venue", "N/A")))}
            <br>
            📅 Date: {html.escape(str(match.get("date", "N/A")))}
          </div>
        </div>
        """

    page += """
      <div style="text-align:center;color:#8496ad;
                  font-size:12px;padding:18px 0 4px;">
        Cricket Live Score Dashboard
      </div>
    </div>
    """
    return page


# ============================================================
# WEBSITE INTERFACE
# ============================================================

with gr.Blocks(
    title="Cricket Live Score Dashboard",
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate"
    )
) as demo:

    gr.Markdown(
        "## 🏏 Cricket Live Score Dashboard\n"
        "Search matches, filter results and refresh scores."
    )

    with gr.Row():
        web_search = gr.Textbox(
            label="🔎 Search",
            placeholder="Team, venue or match name",
            scale=2
        )
        web_status = gr.Dropdown(
            choices=["All", "Live", "Upcoming", "Completed"],
            value="All",
            label="Match Status",
            scale=1
        )

    web_types = sorted({
        str(m.get("matchType", "Unknown")).upper()
        for m in matches
    })

    web_match_type = gr.Dropdown(
        choices=["All"] + web_types,
        value="All",
        label="Match Type"
    )

    with gr.Row():
        web_refresh = gr.Button(
            "🔄 Refresh Scores",
            variant="primary"
        )

    web_output = gr.HTML()

    # Reusable state values for event callbacks
    no_refresh = gr.State(value=False)
    do_refresh = gr.State(value=True)

    # Search and filter events: no API call
    web_search.change(
        fn=make_web_dashboard,
        inputs=[
            web_search, web_status,
            web_match_type, no_refresh
        ],
        outputs=web_output
    )

    web_status.change(
        fn=make_web_dashboard,
        inputs=[
            web_search, web_status,
            web_match_type, no_refresh
        ],
        outputs=web_output
    )

    web_match_type.change(
        fn=make_web_dashboard,
        inputs=[
            web_search, web_status,
            web_match_type, no_refresh
        ],
        outputs=web_output
    )

    # Manual refresh
    web_refresh.click(
        fn=make_web_dashboard,
        inputs=[
            web_search, web_status,
            web_match_type, do_refresh
        ],
        outputs=web_output
    )

    # Initial dashboard display
    demo.load(
        fn=make_web_dashboard,
        inputs=[
            web_search, web_status,
            web_match_type, no_refresh
        ],
        outputs=web_output
    )

    # Auto-refresh every 120 seconds
    web_timer = gr.Timer(value=120, active=True)

    web_timer.tick(
        fn=make_web_dashboard,
        inputs=[
            web_search, web_status,
            web_match_type, do_refresh
        ],
        outputs=web_output
    )

demo.launch(share=True)

# ===== Colab code cell 97 =====
# Step 1: Check the structure of your existing cricket match data

import json
from pprint import pprint

try:
    print("Total matches:", len(matches))

    if len(matches) > 0:
        print("\nFirst match details:")
        pprint(matches[0])
    else:
        print("No match data found. Run your existing backend cell first.")

except NameError:
    print("matches variable not found.")
    print("Run your existing backend/API cell first.")

# ===== Colab code cell 98 =====
import sqlite3
import json
from datetime import datetime

# Database file
DB_PATH = "/content/cricket_dashboard.db"

# Connect to SQLite database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create matches table
cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    match_id TEXT PRIMARY KEY,
    match_name TEXT NOT NULL,
    match_type TEXT,
    match_date TEXT,
    date_time_gmt TEXT,
    venue TEXT,
    status TEXT,
    match_started INTEGER DEFAULT 0,
    match_ended INTEGER DEFAULT 0,
    team1 TEXT,
    team2 TEXT,
    score_json TEXT,
    team_info_json TEXT,
    series_id TEXT,
    raw_json TEXT,
    last_saved TEXT
)
""")

# Save match data from existing matches variable
saved_count = 0

for match in matches:
    teams = match.get("teams") or []

    team1 = teams[0] if len(teams) > 0 else None
    team2 = teams[1] if len(teams) > 1 else None

    cursor.execute("""
        INSERT INTO matches (
            match_id, match_name, match_type, match_date,
            date_time_gmt, venue, status, match_started,
            match_ended, team1, team2, score_json,
            team_info_json, series_id, raw_json, last_saved
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(match_id) DO UPDATE SET
            match_name = excluded.match_name,
            match_type = excluded.match_type,
            match_date = excluded.match_date,
            date_time_gmt = excluded.date_time_gmt,
            venue = excluded.venue,
            status = excluded.status,
            match_started = excluded.match_started,
            match_ended = excluded.match_ended,
            team1 = excluded.team1,
            team2 = excluded.team2,
            score_json = excluded.score_json,
            team_info_json = excluded.team_info_json,
            series_id = excluded.series_id,
            raw_json = excluded.raw_json,
            last_saved = excluded.last_saved
    """, (
        str(match.get("id", "")),
        match.get("name"),
        match.get("matchType"),
        match.get("date"),
        match.get("dateTimeGMT"),
        match.get("venue"),
        match.get("status"),
        int(bool(match.get("matchStarted", False))),
        int(bool(match.get("matchEnded", False))),
        team1,
        team2,
        json.dumps(match.get("score", []), ensure_ascii=False),
        json.dumps(match.get("teamInfo", []), ensure_ascii=False),
        match.get("series_id"),
        json.dumps(match, ensure_ascii=False),
        datetime.now().isoformat(timespec="seconds")
    ))

    saved_count += 1

# Save changes
conn.commit()

# Verify database records
cursor.execute("SELECT COUNT(*) FROM matches")
database_count = cursor.fetchone()[0]

print("Database created successfully!")
print("Database location:", DB_PATH)
print("Matches processed:", saved_count)
print("Matches stored in database:", database_count)

# Show first five records
print("\nSample database records:")

cursor.execute("""
SELECT match_name, match_type, match_date, team1, team2, status
FROM matches
LIMIT 5
""")

for row in cursor.fetchall():
    print(row)

conn.close()

# ===== Colab code cell 99 =====
import sqlite3

# Connect to the existing database
DB_PATH = "/content/cricket_dashboard.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create players table
cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    country TEXT,
    matches_played INTEGER DEFAULT 0,
    runs INTEGER DEFAULT 0,
    wickets INTEGER DEFAULT 0,
    batting_average REAL DEFAULT 0,
    strike_rate REAL DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# Insert sample player data only if the table is empty
cursor.execute("SELECT COUNT(*) FROM players")
player_count = cursor.fetchone()[0]

if player_count == 0:
    sample_players = [
        ("Virat Kohli", "India", 10, 450, 0, 56.25, 145.0),
        ("Rohit Sharma", "India", 10, 380, 0, 42.22, 152.0),
        ("Jasprit Bumrah", "India", 8, 15, 14, 7.50, 90.0),
        ("Babar Azam", "Pakistan", 10, 390, 0, 43.33, 130.0),
        ("Shaheen Afridi", "Pakistan", 8, 12, 12, 6.00, 85.0),
        ("Steve Smith", "Australia", 9, 320, 0, 40.00, 125.0),
        ("Pat Cummins", "Australia", 8, 20, 10, 10.00, 100.0),
        ("Jos Buttler", "England", 10, 410, 0, 45.55, 150.0)
    ]

    cursor.executemany("""
        INSERT INTO players (
            player_name, country, matches_played,
            runs, wickets, batting_average, strike_rate
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, sample_players)

    conn.commit()

# Verify the players table
cursor.execute("SELECT COUNT(*) FROM players")
print("Players table created successfully!")
print("Total sample player records:", cursor.fetchone()[0])

print("\nPlayer Statistics:")
cursor.execute("""
    SELECT player_name, country, matches_played, runs, wickets
    FROM players
    ORDER BY runs DESC
""")

for row in cursor.fetchall():
    print(row)

conn.close()

# ===== Colab code cell 100 =====
import sqlite3

DB_PATH = "/content/cricket_dashboard.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=" * 50)
print("       CRICKET SQL ANALYTICS")
print("=" * 50)

# 1. Top 5 run scorers
print("\n1. TOP RUN SCORERS")
cursor.execute("""
    SELECT player_name, country, runs
    FROM players
    ORDER BY runs DESC
    LIMIT 5
""")
for row in cursor.fetchall():
    print(f"Player: {row[0]} | Country: {row[1]} | Runs: {row[2]}")

# 2. Top wicket takers
print("\n2. TOP WICKET TAKERS")
cursor.execute("""
    SELECT player_name, country, wickets
    FROM players
    ORDER BY wickets DESC
    LIMIT 5
""")
for row in cursor.fetchall():
    print(f"Player: {row[0]} | Country: {row[1]} | Wickets: {row[2]}")

# 3. Number of players by country
print("\n3. PLAYERS BY COUNTRY")
cursor.execute("""
    SELECT country, COUNT(*) AS total_players
    FROM players
    GROUP BY country
    ORDER BY total_players DESC, country
""")
for row in cursor.fetchall():
    print(f"Country: {row[0]} | Players: {row[1]}")

# 4. Match count by match type
print("\n4. MATCHES BY TYPE")
cursor.execute("""
    SELECT match_type, COUNT(*) AS total_matches
    FROM matches
    GROUP BY match_type
    ORDER BY total_matches DESC
""")
for row in cursor.fetchall():
    print(f"Match Type: {row[0]} | Matches: {row[1]}")

# 5. Total matches by completion status
print("\n5. MATCH STATUS SUMMARY")
cursor.execute("""
    SELECT
        CASE
            WHEN match_ended = 1 THEN 'Completed'
            WHEN match_started = 1 THEN 'Live/In Progress'
            ELSE 'Not Started'
        END AS status_group,
        COUNT(*) AS total_matches
    FROM matches
    GROUP BY status_group
    ORDER BY total_matches DESC
""")
for row in cursor.fetchall():
    print(f"Status: {row[0]} | Matches: {row[1]}")

conn.close()

print("\nSQL Analytics completed successfully!")

# ===== Colab code cell 101 =====
import sqlite3

DB_PATH = "/content/cricket_dashboard.db"

def create_player(name, country, matches, runs, wickets):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO players
            (player_name, country, matches_played, runs, wickets)
            VALUES (?, ?, ?, ?, ?)
        """, (name, country, matches, runs, wickets))
    print(f"Player '{name}' added successfully.")

def read_players():
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("""
            SELECT player_id, player_name, country,
                   matches_played, runs, wickets
            FROM players
            ORDER BY player_id
        """).fetchall()

    print("\nPLAYER RECORDS")
    for row in rows:
        print(row)

def update_player(player_id, new_runs):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("""
            UPDATE players
            SET runs = ?
            WHERE player_id = ?
        """, (new_runs, player_id))

    if cursor.rowcount:
        print(f"Player ID {player_id} updated successfully.")
    else:
        print(f"Player ID {player_id} not found.")

def delete_player(player_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("""
            DELETE FROM players
            WHERE player_id = ?
        """, (player_id,))

    if cursor.rowcount:
        print(f"Player ID {player_id} deleted successfully.")
    else:
        print(f"Player ID {player_id} not found.")

# Test READ operation first
read_players()

# ===== Colab code cell 102 =====
# Step 5A: Test CREATE operation

create_player(
    name="Demo Player",
    country="India",
    matches=1,
    runs=50,
    wickets=2
)

# Verify the new record
read_players()

# ===== Colab code cell 103 =====
# Step 5B: Test UPDATE operation

import sqlite3

DB_PATH = "/content/cricket_dashboard.db"

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.execute("""
        UPDATE players
        SET runs = ?
        WHERE player_name = ?
    """, (100, "Demo Player"))

    if cursor.rowcount > 0:
        print("Demo Player updated successfully!")
    else:
        print("Demo Player not found.")

# Verify the updated record
with sqlite3.connect(DB_PATH) as conn:
    result = conn.execute("""
        SELECT player_name, country, matches_played, runs, wickets
        FROM players
        WHERE player_name = ?
    """, ("Demo Player",)).fetchone()

    print("Updated record:", result)

# ===== Colab code cell 104 =====
# Step 5C: Test DELETE operation

import sqlite3

DB_PATH = "/content/cricket_dashboard.db"

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.execute("""
        DELETE FROM players
        WHERE player_name = ?
    """, ("Demo Player",))

    if cursor.rowcount > 0:
        print("Demo Player deleted successfully!")
    else:
        print("Demo Player not found.")

# Verify that Demo Player has been deleted
with sqlite3.connect(DB_PATH) as conn:
    result = conn.execute("""
        SELECT *
        FROM players
        WHERE player_name = ?
    """, ("Demo Player",)).fetchone()

    if result is None:
        print("Verification successful: Demo Player no longer exists.")
    else:
        print("Demo Player still exists:", result)

# ===== Colab code cell 105 =====
import sqlite3

DB_PATH = "/content/cricket_dashboard.db"

queries = [
    # EASY (1-10)
    ("Easy 1: Show all players",
     "SELECT * FROM players"),

    ("Easy 2: Show all match names",
     "SELECT match_name FROM matches"),

    ("Easy 3: Players from India",
     "SELECT * FROM players WHERE country = 'India'"),

    ("Easy 4: Players scoring more than 300 runs",
     "SELECT player_name, runs FROM players WHERE runs > 300"),

    ("Easy 5: Players with at least 10 wickets",
     "SELECT player_name, wickets FROM players WHERE wickets >= 10"),

    ("Easy 6: Matches of type T20",
     "SELECT match_name, match_type FROM matches WHERE LOWER(match_type) = 't20'"),

    ("Easy 7: Count total matches",
     "SELECT COUNT(*) AS total_matches FROM matches"),

    ("Easy 8: Count total players",
     "SELECT COUNT(*) AS total_players FROM players"),

    ("Easy 9: Show completed matches",
     "SELECT match_name, status FROM matches WHERE match_ended = 1"),

    ("Easy 10: Sort players by runs",
     "SELECT player_name, runs FROM players ORDER BY runs DESC"),

    # MEDIUM (11-18)
    ("Medium 11: Top 3 run scorers",
     "SELECT player_name, runs FROM players ORDER BY runs DESC LIMIT 3"),

    ("Medium 12: Top 3 wicket takers",
     "SELECT player_name, wickets FROM players ORDER BY wickets DESC LIMIT 3"),

    ("Medium 13: Player count by country",
     "SELECT country, COUNT(*) FROM players GROUP BY country"),

    ("Medium 14: Average runs per player",
     "SELECT AVG(runs) AS average_runs FROM players"),

    ("Medium 15: Highest and lowest runs",
     "SELECT MAX(runs), MIN(runs) FROM players"),

    ("Medium 16: Matches by match type",
     "SELECT match_type, COUNT(*) FROM matches GROUP BY match_type"),

    ("Medium 17: Matches at each venue",
     "SELECT venue, COUNT(*) FROM matches GROUP BY venue"),

    ("Medium 18: Players with batting average above 40",
     "SELECT player_name, batting_average FROM players WHERE batting_average > 40"),

    # HARD (19-25)
    ("Hard 19: Countries with more than one player",
     """SELECT country, COUNT(*) AS total
        FROM players GROUP BY country HAVING COUNT(*) > 1"""),

    ("Hard 20: Rank players by runs",
     """SELECT player_name, runs,
        RANK() OVER (ORDER BY runs DESC) AS run_rank
        FROM players"""),

    ("Hard 21: Percentage of each country's players",
     """SELECT country, COUNT(*) AS players,
        ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM players), 2) AS percentage
        FROM players GROUP BY country"""),

    ("Hard 22: Match status summary",
     """SELECT CASE
        WHEN match_ended = 1 THEN 'Completed'
        WHEN match_started = 1 THEN 'Live/In Progress'
        ELSE 'Not Started'
        END AS match_status, COUNT(*)
        FROM matches GROUP BY match_status"""),

    ("Hard 23: Players above overall average runs",
     """SELECT player_name, runs FROM players
        WHERE runs > (SELECT AVG(runs) FROM players)"""),

    ("Hard 24: Running total of runs",
     """SELECT player_name, runs,
        SUM(runs) OVER (ORDER BY runs DESC) AS running_total
        FROM players"""),

    ("Hard 25: Matches with team and venue information",
     """SELECT match_name, team1, team2, venue, status
        FROM matches ORDER BY match_date DESC""")
]

with sqlite3.connect(DB_PATH) as conn:
    for title, sql in queries:
        print("\n" + "=" * 60)
        print(title)
        print("-" * 60)

        try:
            cursor = conn.execute(sql)
            rows = cursor.fetchmany(10)

            if rows:
                for row in rows:
                    print(row)
            else:
                print("No records found.")

            if len(rows) == 10:
                print("Showing first 10 rows only.")

        except sqlite3.Error as error:
            print("Query error:", error)

print("\nAll 25 SQL queries have been executed.")

# ===== Colab code cell 106 =====
# Step 7: Create requirements.txt

requirements = """gradio
requests
pandas
"""

with open("/content/requirements.txt", "w") as file:
    file.write(requirements)

print("requirements.txt created successfully!")
print("\nRequired libraries:")
print(requirements)

# ===== Colab code cell 107 =====
from google.colab import files

files.download("/content/requirements.txt")

# ===== Colab code cell 108 =====
# Collect Python code from the current Google Colab notebook
# and save it into one Python file.

from google.colab import files
import json

notebook = get_ipython().user_ns.get("In", [])

# Keep code entered in notebook cells, excluding this collection cell.
current_cell = get_ipython().execution_count

all_code = []

for index, code in enumerate(notebook[1:], start=1):
    if not isinstance(code, str) or not code.strip():
        continue

    # Skip shell/magic commands and empty cells.
    if code.lstrip().startswith(("!", "%")):
        continue

    all_code.append(f"# ===== Colab code cell {index} =====\n")
    all_code.append(code.rstrip() + "\n\n")

output_path = "/content/cricket_project_code.py"

with open(output_path, "w", encoding="utf-8") as f:
    f.writelines(all_code)

print("Python code file created:", output_path)
print("Code cells collected:", len(all_code) // 2)

files.download(output_path)

