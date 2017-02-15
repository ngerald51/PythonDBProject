-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--Create Table for Matches and Players respectively
Create Table playerss(id SERIAL primary key, name TEXT);
Create Table Matches(id SERIAL primary key, winner INTEGER REFERENCES playerss(id), loser INTEGER REFERENCES playerss(id));


CREATE VIEW number_of_wins AS
	SELECT playerss.id, COALESCE(count(matches.winner), 0) as wins 
	from playerss join matches on playerss.id = matches.winner
	where matches.winner = playerss.id group by playerss.id;


--create view to count each players attend how many matches
create view countMatches as
  select players.id as ID,players.name as Name,count(matches.id) as Played
  from players, matches where players.id = matches.winner or players.id = matches.loser
  group by players.id;
  
 --create countWins view to count each players win how many times
create view countWins as
select players.id as ID,players.name as Name,coalesce(count(matches.winner),0) 
as Record
from players left join matches
on players.id = matches.winner
group by players.id;

--create countLoses view to count each players lose how many times
create view countLoses as
select players.id as ID,
       players.name as Name,
       coalesce(count(matches.loser),0) 
as Record
from players left join matches
on players.id = matches.loser
group by players.id;
   
 create view standings as
  select countMatches.ID as ID,
         countMatches.Name as Name,
         coalesce(countWins.Record,0),
         countMatches.Played
  from countMatches left join countWins 
  on countWins.ID = countMatches.ID 
  order by coalesce(countWins.Record) ASC
  ;`