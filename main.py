"""Cricbuzz LiveStats - standalone web application.

Run locally: python -m pip install -r requirements.txt
             python -m streamlit run main.py
"""
from pathlib import Path
import os
import sqlite3

import pandas as pd
import requests
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
DB_DIR = APP_DIR / "database"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "cricbuzz.db"
API_URL = "https://api.cricapi.com/v1/currentMatches"

st.set_page_config(page_title="Cricbuzz LiveStats", page_icon="🏏", layout="wide")


def connect_db():
    conn = sqlite3.connect(str(DB_PATH), timeout=15)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with connect_db() as conn:
        conn.executescript("""
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
            FOREIGN KEY(team_id) REFERENCES teams(team_id) ON DELETE SET NULL
        );
        CREATE TABLE IF NOT EXISTS matches (
            match_id INTEGER PRIMARY KEY AUTOINCREMENT,
            team1_id INTEGER,
            team2_id INTEGER,
            match_date TEXT,
            format TEXT,
            venue TEXT,
            status TEXT,
            winner_team_id INTEGER,
            FOREIGN KEY(team1_id) REFERENCES teams(team_id),
            FOREIGN KEY(team2_id) REFERENCES teams(team_id),
            FOREIGN KEY(winner_team_id) REFERENCES teams(team_id)
        );
        CREATE TABLE IF NOT EXISTS player_stats (
            stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL,
            match_id INTEGER NOT NULL,
            runs INTEGER DEFAULT 0,
            wickets INTEGER DEFAULT 0,
            balls_faced INTEGER DEFAULT 0,
            overs_bowled REAL DEFAULT 0,
            FOREIGN KEY(player_id) REFERENCES players(player_id) ON DELETE CASCADE,
            FOREIGN KEY(match_id) REFERENCES matches(match_id) ON DELETE CASCADE
        );
        """)
        if conn.execute("SELECT COUNT(*) FROM teams").fetchone()[0] == 0:
            conn.executemany("INSERT INTO teams(team_name,country) VALUES(?,?)", [
                ("India", "India"), ("Australia", "Australia"), ("England", "England")
            ])
        if conn.execute("SELECT COUNT(*) FROM players").fetchone()[0] == 0:
            team_map = dict(conn.execute("SELECT team_name,team_id FROM teams").fetchall())
            conn.executemany("INSERT INTO players(player_name,team_id,role) VALUES(?,?,?)", [
                ("Virat Kohli", team_map.get("India"), "Batter"),
                ("Rohit Sharma", team_map.get("India"), "Batter"),
                ("Pat Cummins", team_map.get("Australia"), "Bowler"),
                ("Joe Root", team_map.get("England"), "Batter"),
            ])


def query_df(sql, params=()):
    with connect_db() as conn:
        return pd.read_sql_query(sql, conn, params=params)


def run_sql(sql, params=()):
    with connect_db() as conn:
        conn.execute(sql, params)


def fetch_matches(api_key):
    if not api_key:
        return [], "Enter a valid Cricket API key in the sidebar to request live data."
    try:
        response = requests.get(API_URL, params={"apikey": api_key, "offset": 0}, timeout=20)
        response.raise_for_status()
        payload = response.json()
        if payload.get("status") != "success":
            return [], str(payload.get("reason", "The API did not return success."))
        data = payload.get("data", [])
        return (data if isinstance(data, list) else []), None
    except requests.RequestException as exc:
        return [], f"API request failed: {exc}"
    except ValueError:
        return [], "The API returned an invalid JSON response."


def match_status(match):
    status = str(match.get("status", "")).lower()
    if any(word in status for word in ("live", "in progress", "innings", "stumps", "day ")):
        return "Live"
    if any(word in status for word in ("won by", "draw", "no result", "abandon", "completed")):
        return "Completed"
    return "Upcoming"


def match_row(match):
    teams = match.get("teams", [])
    team_text = " vs ".join(str(t) for t in teams) if isinstance(teams, list) else "Teams unavailable"
    scores = match.get("score", [])
    score_text = "Score unavailable"
    if isinstance(scores, list) and scores:
        parts = []
        for score in scores:
            if isinstance(score, dict):
                parts.append(f"{score.get('r', '?')}/{score.get('w', '?')} ({score.get('o', '?')} overs)")
        if parts:
            score_text = " | ".join(parts)
    return {
        "Match": team_text,
        "Format": str(match.get("matchType", "Unknown")).upper(),
        "Status": match_status(match),
        "Score": score_text,
        "Match Details": match.get("status", "Details unavailable"),
        "Venue": match.get("venue", "Not available"),
        "Date": match.get("date", "Not available"),
    }


init_db()

st.title("🏏 Cricbuzz LiveStats")
st.caption("Cricket scores, player analytics, and SQL-powered database management")

with st.sidebar:
    st.header("Navigation")
    page = st.radio("Open page", ["Live Score Dashboard", "Player Statistics", "Database CRUD", "SQL Query Explorer"])
    st.divider()
    st.subheader("Live Cricket API")
    api_key = st.text_input("Cricket API key", value=os.getenv("CRICKET_API_KEY", ""), type="password")
    auto_refresh = st.checkbox("Auto-refresh every 60 seconds", value=False)
    if st.button("Refresh live data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.caption("Live scores require a valid API key and a plan with API access.")

if auto_refresh:
    try:
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=60_000, key="cricket_refresh")
    except ImportError:
        st.info("To enable auto-refresh, install streamlit-autorefresh from requirements.txt.")

if page == "Live Score Dashboard":
    st.subheader("Live matches")
    matches, api_error = fetch_matches(api_key)
    if api_error:
        st.warning("Live API data is not available right now. The rest of the dashboard can still be used.")
        with st.expander("API diagnostic details"):
            st.write(api_error)
    if matches:
        df = pd.DataFrame([match_row(m) for m in matches])
        a, b, c = st.columns(3)
        a.metric("Matches returned", len(df))
        b.metric("Live", int((df["Status"] == "Live").sum()))
        c.metric("Completed", int((df["Status"] == "Completed").sum()))
        search = st.text_input("Search team, venue, score, or match status")
        status_filter = st.selectbox("Status", ["All", "Live", "Upcoming", "Completed"])
        formats = ["All"] + sorted(df["Format"].dropna().unique().tolist())
        format_filter = st.selectbox("Match format", formats)
        filtered = df.copy()
        if search:
            filtered = filtered[filtered.astype(str).apply(lambda col: col.str.contains(search, case=False, na=False)).any(axis=1)]
        if status_filter != "All":
            filtered = filtered[filtered["Status"] == status_filter]
        if format_filter != "All":
            filtered = filtered[filtered["Format"] == format_filter]
        st.dataframe(filtered, use_container_width=True, hide_index=True)
        st.download_button("Download matches CSV", filtered.to_csv(index=False).encode("utf-8"), "cricket_matches.csv", "text/csv")
    else:
        st.info("No live API matches to display. Verify your API key and account plan. Sample database records are not live scores.")
        st.markdown("**Project modules**")
        st.write("Use Player Statistics, Database CRUD, and SQL Query Explorer from the sidebar while API access is unavailable.")

elif page == "Player Statistics":
    st.subheader("Player leaderboard")
    df = query_df("""
        SELECT p.player_id, p.player_name AS Player,
               COALESCE(t.team_name, 'Unassigned') AS Team,
               COALESCE(p.role, 'Unknown') AS Role,
               COALESCE(SUM(s.runs), 0) AS Runs,
               COALESCE(SUM(s.wickets), 0) AS Wickets,
               COALESCE(SUM(s.balls_faced), 0) AS Balls_Faced,
               COALESCE(SUM(s.overs_bowled), 0) AS Overs_Bowled
        FROM players p LEFT JOIN teams t ON t.team_id=p.team_id
        LEFT JOIN player_stats s ON s.player_id=p.player_id
        GROUP BY p.player_id, p.player_name, t.team_name, p.role
        ORDER BY Runs DESC, Wickets DESC
    """)
    c1, c2, c3 = st.columns(3)
    c1.metric("Players", len(df))
    c2.metric("Recorded runs", int(df["Runs"].sum()) if not df.empty else 0)
    c3.metric("Recorded wickets", int(df["Wickets"].sum()) if not df.empty else 0)
    search = st.text_input("Search player or team")
    if search:
        df = df[df.astype(str).apply(lambda col: col.str.contains(search, case=False, na=False)).any(axis=1)]
    st.dataframe(df.drop(columns=["player_id"], errors="ignore"), use_container_width=True, hide_index=True)
    if not df.empty:
        st.bar_chart(df.set_index("Player")[["Runs", "Wickets"]])
    st.caption("These statistics come from records entered into this project's SQLite database; they are not automatically fetched from the live API.")

elif page == "Database CRUD":
    st.subheader("Database management")
    teams_tab, players_tab, matches_tab, stats_tab = st.tabs(["Teams", "Players", "Matches", "Player Stats"])
    with teams_tab:
        teams = query_df("SELECT * FROM teams ORDER BY team_id")
        st.dataframe(teams, use_container_width=True, hide_index=True)
        with st.form("team_add"):
            name = st.text_input("New team name")
            country = st.text_input("Country")
            submitted = st.form_submit_button("Add team")
        if submitted:
            try:
                if not name.strip():
                    st.error("Team name is required.")
                else:
                    run_sql("INSERT INTO teams(team_name,country) VALUES(?,?)", (name.strip(), country.strip()))
                    st.success("Team added.")
                    st.rerun()
            except sqlite3.IntegrityError as exc:
                st.error(f"Could not add team: {exc}")
        if not teams.empty:
            team_ids = teams["team_id"].tolist()
            chosen = st.selectbox("Team to update/delete", team_ids, format_func=lambda x: f"{x} — {teams.loc[teams.team_id == x, 'team_name'].iloc[0]}")
            old = teams[teams.team_id == chosen].iloc[0]
            with st.form("team_update"):
                new_name = st.text_input("Updated team name", str(old["team_name"]))
                new_country = st.text_input("Updated country", str(old["country"] or ""))
                update = st.form_submit_button("Update team")
            if update:
                try:
                    run_sql("UPDATE teams SET team_name=?, country=? WHERE team_id=?", (new_name.strip(), new_country.strip(), chosen))
                    st.success("Team updated.")
                    st.rerun()
                except sqlite3.IntegrityError as exc:
                    st.error(f"Could not update team: {exc}")
            if st.button("Delete selected team", key="team_delete"):
                try:
                    run_sql("DELETE FROM teams WHERE team_id=?", (chosen,))
                    st.success("Team deleted.")
                    st.rerun()
                except sqlite3.IntegrityError as exc:
                    st.error(f"Could not delete team: {exc}")
    with players_tab:
        players = query_df("SELECT p.player_id,p.player_name,t.team_name,p.team_id,p.role FROM players p LEFT JOIN teams t ON p.team_id=t.team_id ORDER BY p.player_id")
        st.dataframe(players.drop(columns=["team_id"], errors="ignore"), use_container_width=True, hide_index=True)
        teams = query_df("SELECT team_id,team_name FROM teams ORDER BY team_name")
        team_map = {r["team_name"]: int(r["team_id"]) for _, r in teams.iterrows()}
        with st.form("player_add"):
            pname = st.text_input("Player name")
            tname = st.selectbox("Team", ["Unassigned"] + list(team_map))
            role = st.selectbox("Role", ["Batter", "Bowler", "All-rounder", "Wicketkeeper", "Unknown"])
            add = st.form_submit_button("Add player")
        if add:
            if not pname.strip():
                st.error("Player name is required.")
            else:
                run_sql("INSERT INTO players(player_name,team_id,role) VALUES(?,?,?)", (pname.strip(), team_map.get(tname), role))
                st.success("Player added.")
                st.rerun()
        if not players.empty:
            pid = st.selectbox("Player to update/delete", players["player_id"].tolist(), format_func=lambda x: f"{x} — {players.loc[players.player_id == x, 'player_name'].iloc[0]}")
            old = players[players.player_id == pid].iloc[0]
            team_names = ["Unassigned"] + list(team_map)
            current_team = old["team_name"] if pd.notna(old["team_name"]) and old["team_name"] in team_map else "Unassigned"
            role_opts = ["Batter", "Bowler", "All-rounder", "Wicketkeeper", "Unknown"]
            current_role = old["role"] if old["role"] in role_opts else "Unknown"
            with st.form("player_update"):
                new_pname = st.text_input("Updated player name", str(old["player_name"]))
                new_tname = st.selectbox("Updated team", team_names, index=team_names.index(current_team))
                new_role = st.selectbox("Updated role", role_opts, index=role_opts.index(current_role))
                update = st.form_submit_button("Update player")
            if update:
                run_sql("UPDATE players SET player_name=?,team_id=?,role=? WHERE player_id=?", (new_pname.strip(), team_map.get(new_tname), new_role, pid))
                st.success("Player updated.")
                st.rerun()
            if st.button("Delete selected player", key="player_delete"):
                run_sql("DELETE FROM players WHERE player_id=?", (pid,))
                st.success("Player deleted.")
                st.rerun()
    with matches_tab:
        teams = query_df("SELECT team_id,team_name FROM teams ORDER BY team_name")
        team_map = {r["team_name"]: int(r["team_id"]) for _, r in teams.iterrows()}
        matches = query_df("SELECT m.match_id,t1.team_name AS Team_1,t2.team_name AS Team_2,m.match_date,m.format,m.venue,m.status FROM matches m LEFT JOIN teams t1 ON m.team1_id=t1.team_id LEFT JOIN teams t2 ON m.team2_id=t2.team_id ORDER BY m.match_id DESC")
        st.dataframe(matches, use_container_width=True, hide_index=True)
        if len(team_map) >= 2:
            with st.form("match_add"):
                team1 = st.selectbox("Team 1", list(team_map))
                team2 = st.selectbox("Team 2", [x for x in team_map if x != team1])
                match_date = st.date_input("Match date")
                fmt = st.selectbox("Format", ["T20", "ODI", "Test", "Other"])
                venue = st.text_input("Venue")
                status = st.selectbox("Status", ["Scheduled", "Live", "Completed", "Abandoned"])
                add = st.form_submit_button("Add match")
            if add:
                run_sql("INSERT INTO matches(team1_id,team2_id,match_date,format,venue,status) VALUES(?,?,?,?,?,?)", (team_map[team1], team_map[team2], match_date.isoformat(), fmt, venue.strip(), status))
                st.success("Match added.")
                st.rerun()
        else:
            st.info("Add at least two teams to create a match.")
        if not matches.empty:
            mid = st.selectbox("Match to delete", matches["match_id"].tolist())
            if st.button("Delete selected match"):
                run_sql("DELETE FROM matches WHERE match_id=?", (mid,))
                st.success("Match deleted.")
                st.rerun()
    with stats_tab:
        stats = query_df("SELECT s.stat_id,p.player_name AS Player,s.match_id AS Match_ID,s.runs,s.wickets,s.balls_faced,s.overs_bowled FROM player_stats s JOIN players p ON p.player_id=s.player_id ORDER BY s.stat_id DESC")
        st.dataframe(stats, use_container_width=True, hide_index=True)
        players = query_df("SELECT player_id,player_name FROM players ORDER BY player_name")
        matches = query_df("SELECT match_id FROM matches ORDER BY match_id DESC")
        if players.empty or matches.empty:
            st.info("Add a player and a match before entering player statistics.")
        else:
            player_map = {r["player_name"]: int(r["player_id"]) for _, r in players.iterrows()}
            with st.form("stats_add"):
                player_name = st.selectbox("Player", list(player_map))
                match_id = st.selectbox("Match ID", matches["match_id"].tolist())
                runs = st.number_input("Runs", min_value=0, step=1)
                wickets = st.number_input("Wickets", min_value=0, max_value=10, step=1)
                balls = st.number_input("Balls faced", min_value=0, step=1)
                overs = st.number_input("Overs bowled", min_value=0.0, step=0.1)
                add = st.form_submit_button("Add player statistics")
            if add:
                run_sql("INSERT INTO player_stats(player_id,match_id,runs,wickets,balls_faced,overs_bowled) VALUES(?,?,?,?,?,?)", (player_map[player_name], int(match_id), int(runs), int(wickets), int(balls), float(overs)))
                st.success("Statistics added.")
                st.rerun()
        if not stats.empty:
            sid = st.selectbox("Statistics record to delete", stats["stat_id"].tolist())
            if st.button("Delete selected statistics"):
                run_sql("DELETE FROM player_stats WHERE stat_id=?", (sid,))
                st.success("Statistics deleted.")
                st.rerun()

elif page == "SQL Query Explorer":
    st.subheader("Read-only SQL Query Explorer")
    examples = {
        "All teams": "SELECT * FROM teams;",
        "All players with teams": "SELECT p.player_name, t.team_name, p.role FROM players p LEFT JOIN teams t ON p.team_id=t.team_id;",
        "Player run totals": "SELECT p.player_name, COALESCE(SUM(s.runs),0) AS total_runs, COALESCE(SUM(s.wickets),0) AS total_wickets FROM players p LEFT JOIN player_stats s ON s.player_id=p.player_id GROUP BY p.player_id ORDER BY total_runs DESC;",
        "All matches": "SELECT * FROM matches;",
    }
    selected = st.selectbox("Example query", list(examples))
    sql = st.text_area("SQL statement", examples[selected], height=140)
    if st.button("Run query"):
        normalized = sql.strip().rstrip(";").lower()
        if not (normalized.startswith("select ") or normalized.startswith("with ")) or ";" in normalized:
            st.error("Only one read-only SELECT or WITH query is allowed.")
        else:
            try:
                uri = DB_PATH.resolve().as_uri() + "?mode=ro"
                with sqlite3.connect(uri, uri=True) as conn:
                    result = pd.read_sql_query(sql, conn)
                st.dataframe(result, use_container_width=True, hide_index=True)
                st.download_button("Download query results CSV", result.to_csv(index=False).encode("utf-8"), "sql_results.csv", "text/csv")
            except (sqlite3.Error, ValueError) as exc:
                st.error(f"Query failed: {exc}")

st.sidebar.divider()
st.sidebar.caption("Python • Streamlit • SQLite • REST API")
st.caption("Cricbuzz LiveStats — Live score access depends on the API provider and account plan.")
