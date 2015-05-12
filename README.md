PURPOSE:

Emulates Swiss-style tournament. Includes support for:
* Odd number of players (assigning byes, no more than one per player)
* Preventing player rematching

SETUP:

1. Download code from repository and place in desired location.
2. Open a command prompt and navigate to the location above.
3. Execute the following from the command line:
	psql
4. If tournament database has yet to be created, execute the following:
	create database tournament;
5. Execute the following:
	\c tournament
6. Execute the following:
	\i tournament.sql
7. Execute the following:
	\q
8. Execute the following:
	python tournament_test.py
