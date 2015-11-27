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

def registerData(table, column, data):
    """Adds registers to the database, only text values
     Args:
      Data: Data to be inserted.
      Table: Table where the register goes
      Column: Column to insert the register
     Returns:
      "OK" if correctly inserted
      "ERROR" Database error description
    """
    status = "";
      
    db = connect()
    cur = db.cursor()

    query = "INSERT INTO {} ({}) VALUES ('{}')".format(table, column, data)
    
    try:
        cur.execute(query)
    except psycopg2.Error as error:
        status =  error.pgerror
         
    db.commit()
    db.close() 
    
    if (cur.statusmessage == 'INSERT 0 1'):
        status = 'OK'
        
    return status
    

def registerMultipleData(table, **column_data):
    """Adds registers to the database, only numeric values
     Args:
      Data: Data to be inserted.
      Table: Table where the register goes
      Column: Column to insert the register
     Returns:
      "OK" if correctly inserted
      "ERROR" Database error description
    """
    status = "";
  
    db = connect()
    cur = db.cursor()
  
    columns_str = ",".join([str(s) for s in column_data.keys()])
    
    data = list(column_data.values())
    
    for i in range (0,len(column_data)):
        if isinstance(data[i],str):
            data[i] = "'{}'".format(data[i]) 
    
    args_str = ", ".join([str(s) for s in data])   
         
        
    query = "INSERT INTO {} ({}) VALUES ({})".format(table, columns_str,args_str)
    print query
    
    try:
        cur.execute(query)
    except psycopg2.Error as error:
        status =  error.pgerror
        
    db.commit()
    db.close() 
    
    if (cur.statusmessage == 'INSERT 0 1'):
        status = 'OK'
         
    return status
    
def deleteRegisters(table):
    """Remove all the records from the database of a given table.
       Returns:
        "OK"
        "ERROR" Database error description 
    """
        
    status = "OK"
    db = connect()
    cur = db.cursor()
    query = "DELETE FROM %s" % (table,)
    
    try:
        cur.execute(query)
    except psycopg2.Error as error:
        print error.pgerror
        results = error.pgerror
        
    db.commit()
    db.close()       
    
    
def deleteMatches():
    """Remove all the match records from the database.
       Returns:
        "OK"
        "ERROR" Database error description 
    """
    deleteRegisters("matches")  



def deletePlayers():
    """Remove all the player records from the database.
       Returns:
        "OK"
        "ERROR" Database error description 
    """
    return deleteRegisters("players")
    
def deleteTournaments():
    """Remove all the torunaments records from the database.
       Returns:
        "OK"
        "ERROR" Database error description 
    """
        
    return deleteRegisters("tournaments") 

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
  

def registerPlayer(players_name):
    """Adds a player to the tournament database.
     Args:
      name: the player's full name (need not be unique).
     Returns:
      "OK" if correctly inserted
      "ERROR" Database error description
    """
    return registerMultipleData("players", name = players_name)
    #return registerData("players", "name", name)
    
def registerTournament(name):
    """Adds a torunament to the tournament database.
     Args:
      name: the tourament name (need not be unique).
     Returns:
      "ERROR" Database error description
    """
    
    return registerData("tournament", "name", name)    
    
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
    
    return registerMultipleData("matches", (winner,loser,tournament,winner))
    
 
 
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


print (registerPlayer('Osvaldo'))
#print (countPlayers())
#deletePlayers()
#print (reportMatch(23, 26, 1))
#deleteMatches()
#print (registerData("players", "name", "valentin"))