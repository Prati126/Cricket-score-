-- Cricbuzz LiveStats: 25 SQL Practice Questions
-- Database: SQLite
-- Difficulty levels: Easy, Medium, Hard

-- Question 1 [Easy]: List all team names and countries.
SELECT team_name, country FROM teams ORDER BY team_name;

-- Question 2 [Easy]: List all player names and roles.
SELECT player_name, role FROM players ORDER BY player_name;

-- Question 3 [Easy]: Count the total number of teams.
SELECT COUNT(*) AS total_teams FROM teams;

-- Question 4 [Easy]: Count the total number of players.
SELECT COUNT(*) AS total_players FROM players;

-- Question 5 [Easy]: Display all match records.
SELECT * FROM matches;

-- Question 6 [Easy]: List all players belonging to India.
SELECT p.player_name FROM players p JOIN teams t ON p.team_id=t.team_id WHERE t.team_name='India';

-- Question 7 [Easy]: Display each player's name and role.
SELECT player_name, role FROM players;

-- Question 8 [Easy]: Find player performances with at least 50 runs.
SELECT p.player_name, ps.runs FROM player_stats ps JOIN players p ON p.player_id=ps.player_id WHERE ps.runs>=50;

-- Question 9 [Easy]: Find player performances with at least one wicket.
SELECT p.player_name, ps.wickets FROM player_stats ps JOIN players p ON p.player_id=ps.player_id WHERE ps.wickets>=1;

-- Question 10 [Easy]: List all unique match formats.
SELECT DISTINCT format FROM matches;

-- Question 11 [Medium]: Calculate the total runs scored by each player.
SELECT p.player_name, SUM(ps.runs) AS total_runs FROM players p JOIN player_stats ps ON p.player_id=ps.player_id GROUP BY p.player_id,p.player_name;

-- Question 12 [Medium]: Calculate the total wickets taken by each player.
SELECT p.player_name, SUM(ps.wickets) AS total_wickets FROM players p JOIN player_stats ps ON p.player_id=ps.player_id GROUP BY p.player_id,p.player_name;

-- Question 13 [Medium]: Count matches for each format.
SELECT format, COUNT(*) AS total_matches FROM matches GROUP BY format;

-- Question 14 [Medium]: Count players belonging to each team, including teams with no players.
SELECT t.team_name, COUNT(p.player_id) AS player_count FROM teams t LEFT JOIN players p ON t.team_id=p.team_id GROUP BY t.team_id,t.team_name;

-- Question 15 [Medium]: Display the two participating teams for every match.
SELECT m.match_id,t1.team_name AS team1,t2.team_name AS team2 FROM matches m LEFT JOIN teams t1 ON m.team1_id=t1.team_id LEFT JOIN teams t2 ON m.team2_id=t2.team_id;

-- Question 16 [Medium]: Find players with more than 100 total runs.
SELECT p.player_name,SUM(ps.runs) AS total_runs FROM players p JOIN player_stats ps ON p.player_id=ps.player_id GROUP BY p.player_id,p.player_name HAVING SUM(ps.runs)>100;

-- Question 17 [Medium]: Calculate the total recorded runs in each match.
SELECT match_id,SUM(runs) AS total_runs FROM player_stats GROUP BY match_id;

-- Question 18 [Medium]: Calculate each player's average runs per recorded performance.
SELECT p.player_name,ROUND(AVG(ps.runs),2) AS average_runs FROM players p JOIN player_stats ps ON p.player_id=ps.player_id GROUP BY p.player_id,p.player_name;

-- Question 19 [Hard]: Find the top five players by total runs.
SELECT p.player_name,SUM(ps.runs) AS total_runs FROM players p JOIN player_stats ps ON p.player_id=ps.player_id GROUP BY p.player_id,p.player_name ORDER BY total_runs DESC LIMIT 5;

-- Question 20 [Hard]: Find the top three players by total wickets.
SELECT p.player_name,SUM(ps.wickets) AS total_wickets FROM players p JOIN player_stats ps ON p.player_id=ps.player_id GROUP BY p.player_id,p.player_name ORDER BY total_wickets DESC LIMIT 3;

-- Question 21 [Hard]: Find the highest-scoring player in each match, including ties.
WITH scores AS (SELECT ps.match_id,p.player_name,ps.runs,RANK() OVER(PARTITION BY ps.match_id ORDER BY ps.runs DESC) AS rnk FROM player_stats ps JOIN players p ON p.player_id=ps.player_id) SELECT match_id,player_name,runs FROM scores WHERE rnk=1;

-- Question 22 [Hard]: Find players who have recorded both runs and wickets.
SELECT p.player_name,SUM(ps.runs) AS total_runs,SUM(ps.wickets) AS total_wickets FROM players p JOIN player_stats ps ON p.player_id=ps.player_id GROUP BY p.player_id,p.player_name HAVING SUM(ps.runs)>0 AND SUM(ps.wickets)>0;

-- Question 23 [Hard]: Calculate total runs scored by players from each team.
SELECT COALESCE(t.team_name,'Unknown Team') AS team_name,SUM(ps.runs) AS total_runs FROM player_stats ps JOIN players p ON ps.player_id=p.player_id LEFT JOIN teams t ON p.team_id=t.team_id GROUP BY t.team_id,t.team_name;

-- Question 24 [Hard]: Find matches whose total recorded runs exceed the average match total.
WITH totals AS (SELECT match_id,SUM(runs) AS total_runs FROM player_stats GROUP BY match_id) SELECT match_id,total_runs FROM totals WHERE total_runs>(SELECT AVG(total_runs) FROM totals);

-- Question 25 [Hard]: Rank players by total runs, assigning equal ranks to tied totals.
WITH totals AS (SELECT p.player_name,SUM(ps.runs) AS total_runs FROM players p JOIN player_stats ps ON p.player_id=ps.player_id GROUP BY p.player_id,p.player_name) SELECT player_name,total_runs,DENSE_RANK() OVER(ORDER BY total_runs DESC) AS player_rank FROM totals;

