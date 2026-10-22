# Cricbuzz LiveStats - 25 SQL Practice Questions and Answers

Database: SQLite

Tables: `teams`, `players`, `matches`, `player_stats`


## Easy Level

### Question 1: List all team names and countries.

**Answer:**

```sql
SELECT team_name, country FROM teams ORDER BY team_name;
```

### Question 2: List all player names and roles.

**Answer:**

```sql
SELECT player_name, role FROM players ORDER BY player_name;
```

### Question 3: Count the total number of teams.

**Answer:**

```sql
SELECT COUNT(*) AS total_teams FROM teams;
```

### Question 4: Count the total number of players.

**Answer:**

```sql
SELECT COUNT(*) AS total_players FROM players;
```

### Question 5: Display all match records.

**Answer:**

```sql
SELECT * FROM matches;
```

### Question 6: List all players belonging to India.

**Answer:**

```sql
SELECT p.player_name FROM players p JOIN teams t ON p.team_id=t.team_id WHERE t.team_name='India';
```

### Question 7: Display each player's name and role.

**Answer:**

```sql
SELECT player_name, role FROM players;
```

### Question 8: Find player performances with at least 50 runs.

**Answer:**

```sql
SELECT p.player_name, ps.runs FROM player_stats ps JOIN players p ON p.player_id=ps.player_id WHERE ps.runs>=50;
```

### Question 9: Find player performances with at least one wicket.

**Answer:**

```sql
SELECT p.player_name, ps.wickets FROM player_stats ps JOIN players p ON p.player_id=ps.player_id WHERE ps.wickets>=1;
```

### Question 10: List all unique match formats.

**Answer:**

```sql
SELECT DISTINCT format FROM matches;
```


## Medium Level

### Question 11: Calculate the total runs scored by each player.

**Answer:**

```sql
SELECT p.player_name, SUM(ps.runs) AS total_runs FROM players p JOIN player_stats ps ON p.player_id=ps.player_id GROUP BY p.player_id,p.player_name;
```

### Question 12: Calculate the total wickets taken by each player.

**Answer:**

```sql
SELECT p.player_name, SUM(ps.wickets) AS total_wickets FROM players p JOIN player_stats ps ON p.player_id=ps.player_id GROUP BY p.player_id,p.player_name;
```

### Question 13: Count matches for each format.

**Answer:**

```sql
SELECT format, COUNT(*) AS total_matches FROM matches GROUP BY format;
```

### Question 14: Count players belonging to each team, including teams with no players.

**Answer:**

```sql
SELECT t.team_name, COUNT(p.player_id) AS player_count FROM teams t LEFT JOIN players p ON t.team_id=p.team_id GROUP BY t.team_id,t.team_name;
```

### Question 15: Display the two participating teams for every match.

**Answer:**

```sql
SELECT m.match_id,t1.team_name AS team1,t2.team_name AS team2 FROM matches m LEFT JOIN teams t1 ON m.team1_id=t1.team_id LEFT JOIN teams t2 ON m.team2_id=t2.team_id;
```

### Question 16: Find players with more than 100 total runs.

**Answer:**

```sql
SELECT p.player_name,SUM(ps.runs) AS total_runs FROM players p JOIN player_stats ps ON p.player_id=ps.player_id GROUP BY p.player_id,p.player_name HAVING SUM(ps.runs)>100;
```

### Question 17: Calculate the total recorded runs in each match.

**Answer:**

```sql
SELECT match_id,SUM(runs) AS total_runs FROM player_stats GROUP BY match_id;
```

### Question 18: Calculate each player's average runs per recorded performance.

**Answer:**

```sql
SELECT p.player_name,ROUND(AVG(ps.runs),2) AS average_runs FROM players p JOIN player_stats ps ON p.player_id=ps.player_id GROUP BY p.player_id,p.player_name;
```


## Hard Level

### Question 19: Find the top five players by total runs.

**Answer:**

```sql
SELECT p.player_name,SUM(ps.runs) AS total_runs FROM players p JOIN player_stats ps ON p.player_id=ps.player_id GROUP BY p.player_id,p.player_name ORDER BY total_runs DESC LIMIT 5;
```

### Question 20: Find the top three players by total wickets.

**Answer:**

```sql
SELECT p.player_name,SUM(ps.wickets) AS total_wickets FROM players p JOIN player_stats ps ON p.player_id=ps.player_id GROUP BY p.player_id,p.player_name ORDER BY total_wickets DESC LIMIT 3;
```

### Question 21: Find the highest-scoring player in each match, including ties.

**Answer:**

```sql
WITH scores AS (SELECT ps.match_id,p.player_name,ps.runs,RANK() OVER(PARTITION BY ps.match_id ORDER BY ps.runs DESC) AS rnk FROM player_stats ps JOIN players p ON p.player_id=ps.player_id) SELECT match_id,player_name,runs FROM scores WHERE rnk=1;
```

### Question 22: Find players who have recorded both runs and wickets.

**Answer:**

```sql
SELECT p.player_name,SUM(ps.runs) AS total_runs,SUM(ps.wickets) AS total_wickets FROM players p JOIN player_stats ps ON p.player_id=ps.player_id GROUP BY p.player_id,p.player_name HAVING SUM(ps.runs)>0 AND SUM(ps.wickets)>0;
```

### Question 23: Calculate total runs scored by players from each team.

**Answer:**

```sql
SELECT COALESCE(t.team_name,'Unknown Team') AS team_name,SUM(ps.runs) AS total_runs FROM player_stats ps JOIN players p ON ps.player_id=p.player_id LEFT JOIN teams t ON p.team_id=t.team_id GROUP BY t.team_id,t.team_name;
```

### Question 24: Find matches whose total recorded runs exceed the average match total.

**Answer:**

```sql
WITH totals AS (SELECT match_id,SUM(runs) AS total_runs FROM player_stats GROUP BY match_id) SELECT match_id,total_runs FROM totals WHERE total_runs>(SELECT AVG(total_runs) FROM totals);
```

### Question 25: Rank players by total runs, assigning equal ranks to tied totals.

**Answer:**

```sql
WITH totals AS (SELECT p.player_name,SUM(ps.runs) AS total_runs FROM players p JOIN player_stats ps ON p.player_id=ps.player_id GROUP BY p.player_id,p.player_name) SELECT player_name,total_runs,DENSE_RANK() OVER(ORDER BY total_runs DESC) AS player_rank FROM totals;
```

