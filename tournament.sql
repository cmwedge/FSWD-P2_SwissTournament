-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dAShes, like
-- these lines here.

--Tracks players
CREATE TABLE Player (
	ID SERIAL PRIMARY KEY,
	Name VARCHAR(50) NOT NULL
);

--Tracks matches between players
CREATE TABLE Match (
	ID SERIAL PRIMARY KEY,
	Winner INT REFERENCES Player (ID) NOT NULL,
	Loser INT REFERENCES Player (ID)
);

--View for tracking player standings
CREATE VIEW PlayerStandings AS
SELECT	ID,
	Name,
	(SELECT COUNT(*)
	 FROM   Match
	 WHERE  Winner = p.ID) AS Wins,
	(SELECT COUNT(*)
	 FROM   Match
	 WHERE  Winner = p.ID
	    OR  Loser = p.ID) AS Matches
FROM	Player p
ORDER BY 
	Wins DESC;
