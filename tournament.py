###############################################################################
# File: Tournament.py
# Author: Juana De La Cuesta
# 
# tournament.py -- implementation of a Swiss-system tournament
#
###############################################################################
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database.
       Returns:
        "OK"
        "ERROR" Database error description 
    """
        
    status = "OK"
    db = connect()
    cur = db.cursor()
    
    try:
        cur.execute("DELETE FROM matches")
    except psycopg2.Error as error:
        print error.pgerror
        results = error.pgerror
        
    db.commit()
    db.close() 


def deletePlayers():
    """Remove all the player records from the database.
       Returns:
        "OK"
        "ERROR" Database error description 
    """
        
    status = "OK"
    db = connect()
    cur = db.cursor()
    
    try:
        cur.execute("DELETE FROM players")
    except psycopg2.Error as error:
        print error.pgerror
        results = error.pgerror
        
    db.commit()
    db.close() 
    

def countPlayers():
    """Returns the number of players currently registered.
       Returns:
        A one value tuple with number of players in the database
        ERROR - Problems with the database
        """
        
    db = connect()
    cur = db.cursor()
    
    try:
        cur.execute("SELECT count(*) FROM players")
        results = cur.fetchall()
        results = results[0]
    except psycopg2.Error as error:
        #print error.pgerror
        results = 'ERROR - Problems with the database'
        
    db.commit()
    db.close() 
    return (results)
  

def registerPlayer(name):
    """Adds a player to the tournament database.
     Args:
      name: the player's full name (need not be unique).
     Returns:
      "OK" if correctly inserted
      "ERROR - Name blank" if the name is blank
      "ERROR - Problems with the database, data not saved"
    """
    status = "";
    
    if not(name):
        status = 'ERROR - Name blank' 
        return status
        
    db = connect()
    cur = db.cursor()
    
    try:
        cur.execute("INSERT INTO players (name) VALUES (%s)",(name,))
    except psycopg2.Error as error:
        status =  error.pgerror
         
    db.commit()
    db.close() 
    
    if (cur.statusmessage == 'INSERT 0 1'):
        status = 'OK'
        
    return status
    
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


def reportMatch(winner, loser, tournament):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tourament: Id of the tournament the match belongs to 
    Returns:
      "OK" if correctly inserted
      "ERROR" Database error description
    """
    status = "";
    
    db = connect()
    cur = db.cursor()
    args = [winner, loser, tournament, winner]
    query = ("INSERT INTO matches VALUES (%s, %s, %s, %s)")
    try:
        cur.execute(query,args)
        
    except psycopg2.Error as error:
        status =  error.pgerror
         
    db.commit()
    db.close() 
    
    if (cur.statusmessage == 'INSERT 0 1'):
        status = 'OK'
        
    return status    
 
 
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

#print (registerPlayer('juan'))
#print (countPlayers())
#deletePlayers()
print (reportMatch(23, 26, 1))
deleteMatches()
