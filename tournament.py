#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  
    
    Returns a database connection.
    """
    return psycopg2.connect("dbname=tournament")

def delete_matches():
    """Remove all the match records from the database."""
    db = connect()
    crsr = db.cursor()
    crsr.execute("delete from Match;")
    db.commit()

def delete_players():
    """Remove all the player records from the database."""
    db = connect()
    crsr = db.cursor()
    crsr.execute("delete from Player;")
    db.commit()

def count_players():
    """Returns the number of players currently registered."""
    db = connect()
    crsr = db.cursor()
    crsr.execute("select count(*) from Player;")
    return int(crsr.fetchall()[0][0])

def register_player(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.
    (This should be handled by your SQL database schema, not in your
    Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    crsr = db.cursor()
    crsr.execute("insert into Player (Name) values (%s);", (name,))
    db.commit()


def player_standings():
    """Returns a list of the players and their win records, sorted by
    wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains 
      (id, name, wins, matches, byes):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
        byes: the number of byes a player has received
    """

    db = connect()
    crsr = db.cursor()
    crsr.execute(("select * from PlayerStandings;"))
    rows = crsr.fetchall()
    ps = [(row[0], row[1], row[2], row[3])
          for row in rows]
    return ps


def report_match(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    crsr = db.cursor()
    crsr.execute("insert into Match (Winner, Loser) values (%s, %s);",
                 (winner, loser))
    db.commit()

def get_matches():
    """Gets all recorded matches.
    
    Returns:
      A dictionary mapping player ID to a list of opponent IDs.
    """
    db = connect()
    crsr = db.cursor()
    crsr.execute("select winner, loser from Match")
    rows = crsr.fetchall()
    player_matches = {}
    for row in rows:
        player, opponent = row[0], row[1]
        if player not in player_matches:
            player_matches[player] = []
        if opponent not in player_matches:
            player_matches[opponent] = []
        if player not in player_matches[opponent]:
            player_matches[opponent].append(player)
        if opponent not in player_matches[player]:
            player_matches[player].append(opponent)

    return player_matches

def swiss_pairings():
    """Returns a list of pairs of players for the next round.
  
    Each player is paired with another player with an equal or
    nearly-equal win record, that is, a player adjacent to him
    or her in the standings.

    Players will not be rematched.

    Supports byes which are assigned to the player with lowest
    overall score who hasn't received a bye.
  
    Returns:
      A list of tuples, each of which contains 
      (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    ps = player_standings()
    matches = get_matches()
    unmatched = set((player[0] for player in ps))
    next_round = []

    #if odd number of participants, assign bye
    if len(unmatched) % 2 == 1:
        for i in range(len(ps)-1, -1, -1):
            if None not in matches[ps[i][0]]:
                next_round.append((ps[i][0], ps[i][1], None, "BYE"))
                unmatched.remove(ps[i][0])
                break

    #generate matches
    while len(unmatched) > 0:
        p1, p2 = None, None
        for i in range(len(ps)):
            if ps[i][0] in unmatched:
                p1, p1Name = ps[i][0], ps[i][1]
                for j in range(i+1, len(ps)):
                    if ps[j][0] in unmatched:
                        #check if p1 has already played this player
                        if ps[j][0] not in matches[p1]:
                            p2, p2Name = ps[j][0], ps[j][1]
                            break
                break

        next_round.append((p1, p1Name, p2, p2Name))
        unmatched.remove(p1)
        unmatched.remove(p2)

    return next_round