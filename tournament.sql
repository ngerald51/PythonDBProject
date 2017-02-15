-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


Create Table Players(id SERIAL primary key, name TEXT);
Create Table Matches(id SERIAL primary key, winner INTEGER REFERENCES players(id), loser INTEGER REFERENCES players(id));

Create View win_total as 
select players.id, players.name, count(players.id) as wintotal, 
count (matches.winner + matches.loser) as matches_played from players,
matches where players.id=matches.winner group by players.id order by wintotal desc;

Create VIEW WIN_ALT as
select players.id, players.name, count(players.id) as wintotal, 
count (matches.winner + matches.loser) as matches_played from players,
matches where players.id=matches.winner or player.id=matches.loser group by players.id order by wintotal desc;
