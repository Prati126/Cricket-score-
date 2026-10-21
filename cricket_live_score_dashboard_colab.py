# Cricket Live Score Dashboard — Google Colab
# Run this cell after your API request cell has created `result`.

import pandas as pd
from IPython.display import display, HTML

# Validate the API response
if "result" not in globals() or not isinstance(result, dict):
    raise ValueError("আগের API request cell চালাও, যাতে `result` variable তৈরি হয়।")

if result.get("status") != "success":
    raise ValueError(f"API সফল response দেয়নি। Status: {result.get('status')}")

matches = result.get("data", [])
if not isinstance(matches, list):
    raise ValueError("API response-এর `data` field একটি list নয়।")

def score_text(match):
    score_items = match.get("score") or []
    if not score_items:
        return "Score not available"

    parts = []
    for item in score_items:
        if not isinstance(item, dict):
            continue
        inning = item.get("inning") or item.get("team") or "Innings"
        runs = item.get("r", "?")
        wickets = item.get("w", "?")
        overs = item.get("o", "?")
        parts.append(f"{inning}: {runs}/{wickets} ({overs} ov)")
    return " · ".join(parts) if parts else "Score not available"

def team_names(match):
    teams = match.get("teams") or []
    if isinstance(teams, list) and teams:
        return " vs ".join(str(t) for t in teams)
    return match.get("name") or "Teams unavailable"

def safe(value, fallback="—"):
    if value is None or value == "":
        return fallback
    return str(value)

# Create the table data
rows = []
for match in matches:
    rows.append({
        "Match": safe(match.get("name")),
        "Match Type": safe(match.get("matchType")),
        "Teams": team_names(match),
        "Score": score_text(match),
        "Status": safe(match.get("status")),
        "Venue": safe(match.get("venue")),
        "Date": safe(match.get("date")),
    })

df = pd.DataFrame(rows)

# Dashboard styling
cards_html = []
for match in matches:
    name = safe(match.get("name"), "Match")
    match_type = safe(match.get("matchType"), "Cricket")
    status = safe(match.get("status"), "Status unavailable")
    venue = safe(match.get("venue"), "Venue unavailable")
    date = safe(match.get("date"), "Date unavailable")
    scores = score_text(match)
    teams = team_names(match)

    # Escape API-provided text before inserting into HTML
    import html
    name, match_type, status, venue, date, scores, teams = [
        html.escape(x) for x in (name, match_type, status, venue, date, scores, teams)
    ]

    status_lower = status.lower()
    if "won" in status_lower or "result" in status_lower:
        badge = "COMPLETED"
    elif any(word in status_lower for word in ("live", "in progress", "innings", "stumps")):
        badge = "LIVE / IN PLAY"
    else:
        badge = "MATCH"

    cards_html.append(f"""
      <article class="match-card">
        <div class="card-top">
          <span class="competition">{match_type}</span>
          <span class="badge">{badge}</span>
        </div>
        <h3>{name}</h3>
        <div class="teams">{teams}</div>
        <div class="score">{scores}</div>
        <p class="status">{status}</p>
        <div class="meta">📍 {venue}</div>
        <div class="meta">📅 {date}</div>
      </article>
    """)

cards = "\n".join(cards_html) if cards_html else """
  <div class="empty">এই response-এ কোনও ম্যাচ পাওয়া যায়নি। API response আবার পরীক্ষা করো।</div>
"""

dashboard_html = f"""
<style>
.cricket-app {{
  font-family: Inter, system-ui, -apple-system, Segoe UI, sans-serif;
  color: #eef4ff; background: #0b1220; padding: 22px;
  border-radius: 18px; max-width: 1200px; margin: 8px auto;
}}
.cricket-hero {{
  padding: 24px; border-radius: 16px;
  background: linear-gradient(120deg, #123b32, #16264c);
  border: 1px solid #31544e; margin-bottom: 18px;
}}
.cricket-kicker {{ color: #9be7bd; font-size: 12px; font-weight: 800; letter-spacing: 2px; }}
.cricket-hero h2 {{ margin: 8px 0; font-size: 30px; color: white; }}
.cricket-hero p {{ margin: 0; color: #c9d7e9; }}
.cricket-stats {{ display: flex; flex-wrap: wrap; gap: 12px; margin: 16px 0 24px; }}
.stat {{ flex: 1 1 130px; padding: 16px; background: #151f31; border: 1px solid #29364c; border-radius: 12px; }}
.stat strong {{ display: block; font-size: 26px; color: #a6f0c1; }}
.stat span {{ color: #b7c4d8; font-size: 13px; }}
.section-title {{ color: white; margin: 22px 0 12px; font-size: 20px; }}
.match-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; }}
.match-card {{ background: #151f31; border: 1px solid #2a3950; border-radius: 14px; padding: 17px; min-width: 0; }}
.card-top {{ display: flex; align-items: center; justify-content: space-between; gap: 8px; }}
.competition {{ color: #a9b8ce; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }}
.badge {{ background: #203d32; color: #a6f0c1; border: 1px solid #35624d; border-radius: 999px; padding: 4px 8px; font-size: 10px; font-weight: 800; }}
.match-card h3 {{ color: white; font-size: 17px; line-height: 1.4; margin: 14px 0 8px; }}
.teams {{ color: #b8c7db; font-size: 12px; }}
.score {{ color: #a6f0c1; font-size: 14px; font-weight: 750; line-height: 1.6; margin-top: 14px; overflow-wrap: anywhere; }}
.status {{ color: #f1f5fb; font-size: 13px; line-height: 1.5; }}
.meta {{ color: #94a6bd; font-size: 12px; line-height: 1.6; overflow-wrap: anywhere; }}
.empty {{ padding: 20px; color: #cbd5e1; }}
.note {{ color: #9baec6; font-size: 12px; margin-top: 18px; line-height: 1.5; }}
</style>
<div class="cricket-app">
  <header class="cricket-hero">
    <div class="cricket-kicker">CRICKET • LIVE DATA</div>
    <h2>Cricket Scoreboard</h2>
    <p>Current matches, score details and match status in one place.</p>
  </header>
  <div class="cricket-stats">
    <div class="stat"><strong>{len(matches)}</strong><span>Matches returned by API</span></div>
    <div class="stat"><strong>{sum(1 for m in matches if any(w in str(m.get('status','')).lower() for w in ('live','in progress','innings','stumps')))}</strong><span>Potentially live / in-play</span></div>
    <div class="stat"><strong>{sum(1 for m in matches if 'won' in str(m.get('status','')).lower() or 'result' in str(m.get('status','')).lower())}</strong><span>Results indicated by status</span></div>
  </div>
  <h3 class="section-title">Matches</h3>
  <div class="match-grid">{cards}</div>
  <p class="note">Note: This dashboard displays the API response as received. It does not independently verify match authenticity or guarantee real-time updates. Run the API request cell again to refresh the data.</p>
</div>
"""

display(HTML(dashboard_html))

print(f"Match table — {len(df)} matches")
display(df)
