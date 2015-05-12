-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--Tracks players
create table Player (
	ID serial PRIMARY KEY,
	Name varchar(50) NOT NULL
);

--Tracks matches between players
create table Match (
	ID serial PRIMARY KEY,
	Winner int REFERENCES Player (ID) NOT NULL,
	Loser int REFERENCES Player (ID)
);

--View for tracking player standings
create view PlayerStandings as
select	ID,
		Name,
		(select count(*)
		 from   Match
		 where  Winner = p.ID) as Wins,
		(select count(*)
		 from   Match
		 where  Winner = p.ID
			or  Loser = p.ID) as Matches
from	Player p
order by 
		Wins desc;