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

  
def close_connection(connection):
    """Desonnect from the PostgreSQL database."""
    connection.close()


def commit_connection(connection):
    """Commit to the PostgreSQL database."""
    connection.commit()

    
def registerMultipleData(table, **column_data):
    """Adds registers to the database, the specified column = data to the table
     Args:
      **column_data: Dictionary with the column = value to be inserted
      table: Table where the register goes
     Returns:
      "OK" if correctly inserted
      "ERROR" Database error description
    """
    status = "OK";
    db = connect()
    cur = db.cursor()
 
    columns_str = ", ".join([str(s) for s in column_data.keys()])
    args_str = ", ".join(["%(" + str(s) + ")s" for s in column_data.keys()])
   
# Format the query to be executed     
    query = "INSERT INTO {} ({}) VALUES ({})".format(table, columns_str, 
    args_str)

    try:
        cur.execute(query, column_data)
        
    except psycopg2.Error as error:
        status =  error.pgerror
    
    commit_connection(db)
    close_connection(db) 

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
    query = "DELETE FROM {}".format(table)
    try:
        cur.execute(query)
    except psycopg2.Error as error:
        status = error.pgerror
        
    commit_connection(db)
    close_connection(db)     
    return status
 
    
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
        results = results[0][0]
    except psycopg2.Error as error:
        #print error.pgerror
        results = 'ERROR - Problems with the database'
        
    commit_connection(db)
    close_connection(db) 
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
    
def registerTournament(tournament_name):
    """Adds a torunament to the tournament database.
     Args:
      name: the tourament name (need not be unique).
     Returns:
      "ERROR" Database error description
    """
 
    return registerMultipleData("tournaments", name = tournament_name)    
   

def reportMatch(winner, loser, tournament, tie_result = False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tournament: Id of the tournament the match belongs to 
    Returns:
      "OK" if correctly inserted
      "ERROR" Database error description
      "ERROR - Game duplicated" If the game is already in the database
    """
    if not (checkExistanceOfMatch(winner, loser, tournament)):
        return registerMultipleData("matches", winner_ID = winner,\
        loser_ID = loser, tournament_ID = tournament, tie = tie_result)
    
    else:
        return "ERROR - Game duplicated"
    
    
def checkExistanceOfMatch(winner, loser, tournament):
    """Checks if a particular game from a particular tournament is already in 
       the database
       
       Returns:
        False if the game is not present
        True if the game is already present 
    """
 
# Check the existance of the game in the database, disregard of the results 
    db = connect()
    cur = db.cursor()
    query = "SELECT count(*) FROM matches WHERE tournament_ID = {} AND (\
    (winner_ID = {} AND loser_ID = {}) OR (winner_ID = {} AND loser_ID = {}))".\
    format(tournament, winner, loser, loser, winner)
    
    cur.execute(query)
    results = cur.fetchall() 
    close_connection(db) 
    
    if results[0][0]:
        return True        
    else:  
       return False
        

def playerStandings(tournament = 0):
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
    db = connect()
    cur = db.cursor()
#Check if the petition is from an specific tournament or for all players    
    if(tournament):
        query = "SELECT name, games.player_ID, games, wins FROM games, wins\
        WHERE wins.player_ID = games.player_ID AND tournament_ID = {} \
        ORDER BY wins DESC".format(tournament)
        
    else:
        query = "SELECT name, games.player_ID, games, wins FROM games, wins\
        WHERE wins.player_ID = games.player_ID ORDER BY wins DESC"
    
    cur.execute(query)
    results = cur.fetchall() 
    close_connection(db)  

    return [(row[1], row[0], row[3], row[2]) for row in results]  
    
         
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

#deleteMatches() 
#print (registerPlayer("12343 o'barca"))

#print (registerTournament('Karate'))
#
#print (reportMatch(356, 370, 24, True))

#print (reportMatch(234,235, 22, True))    

'''for i in range (71,90):
    print (reportMatch(i+10, i-5, 2, False))
    
for i in range (0,10):
    print (registerPlayer('julia'+ str(i)))

for i in range (0,20):
    print (registerPlayer('Karla'+ str(i)))    
    
print (registerTournament('Ping pong'))
   
for i in range (68,80):
    print (reportMatch(i, i+3, 1, False))
    
for i in range (100,114):
    print (reportMatch(i-30,i, 1, True))    
 
for i in range (88,101):
    print (reportMatch(i-3,i+2, 1, True))   
 '''
  
#print (registerTournament('Ping pong'))
#print (countPlayers())
#print deletePlayers()
#print (reportMatch(1,0, 7, True))
#print (checkExistanceOfMatch(70, 80, 7))
#print playerStandings()
