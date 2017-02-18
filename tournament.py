#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")




def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    query = "UPDATE player_stats SET matches='0', wins='0', rating='0';"
    c.execute(query)
    conn.commit() 
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    query = "DELETE from player_stats;"
    c.execute(query)
    conn.commit() 
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    query = "SELECT COUNT(id) FROM player_stats;"
    c.execute(query)
    number = c.fetchall()[0][0]
    conn.close()        
    return number


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    name = str(bleach.clean(name))
    query = "INSERT INTO player_stats (name, matches, wins, rating) VALUES (%s, '0', '0', '0');"
    c.execute(query, (name,))
    conn.commit()
    conn.close()
    

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    query = "SELECT id, name, wins, matches FROM player_stats ORDER BY wins DESC;"
    c.execute(query)
    standings = c.fetchall()
    conn.close()        
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    
    query = "SELECT matches, wins, rating FROM player_stats WHERE id = %s;"
    c.execute(query, (winner,))
    starting_stats = c.fetchall()
    matches = starting_stats[0][0]+1
    wins = starting_stats[0][1]+1
    rating = float(wins) / matches * 100
    query = "UPDATE player_stats SET matches=%s, wins=%s, rating=%s WHERE id = %s;"
    c.execute(query, (matches, wins, rating, winner, ))

    query = "SELECT matches, wins, rating FROM player_stats WHERE id = %s;"
    c.execute(query, (loser,))
    starting_stats = c.fetchall()
    matches = starting_stats[0][0]+1
    wins = starting_stats[0][1]
    rating = float(wins) / matches * 100
    query = "UPDATE player_stats SET matches=%s, wins=%s, rating=%s WHERE id = %s;"
    c.execute(query, (matches, wins, rating, loser, ))

    conn.commit()
    conn.close()
    



    #query = "UPDATE player_stats SET matches=+'1', wins=+'1', rating='0' where id ='1';"
    #c.execute(query, (name,))
    
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """


