# Tournament
Second project for teh Udacity full Stack Nano Degree

In order to access the functions built in the tournament.py
file, clone the repository and use the Postgres console 
to import the tournament.sql file in order to create the 
database. The command to do so is: 
    psql -f tournament.sql
    
Import the module to your file and that´s it. The functions in the file are the
following:


def connect():
    Connect to the PostgreSQL database.  
    Returns a database connection.

def close_connection(connection):
    Desonnect from the PostgreSQL database.

def commit_connection(connection):
    Commit to the PostgreSQL database."""
    connection.commit()

    Example of a connection:

        db = connect()
        cur = db.cursor()
        query = "DELETE FROM table_name"
        try:
            cur.execute(query)
        except psycopg2.Error as error:
            status = error.pgerror

        commit_connection(db)
        close_connection(db)
        

def registerMultipleData(table, **column_data):
    Adds registers to the database, the specified column = data to the table
     Args:
      **column_data: Dictionary with the column = value to be inserted
      table: Table where the register goes
     Returns:
      "OK" if correctly inserted
      "ERROR" Database error description


def deleteRegisters(table):
    Remove all the records from the database of a given table.
    Args:
      table: Table to erase the registers from
      Returns:
       "OK"
       "ERROR" Database error description


def deleteMatches():
    Remove all the match records from the database.
       Returns:
        "OK"
        "ERROR" Database error description


def deletePlayers():
    Remove all the player records from the database.
       Returns:
        "OK"
        "ERROR" Database error description
    
    
def deleteTournaments():
    Remove all the torunaments records from the database.
       Returns:
        "OK"
        "ERROR" Database error description


def countPlayers():
    Returns the number of players currently registered.
       Returns:
        A one value tuple with number of players in the database
        ERROR - Problems with the database
     

def registerPlayer(players_name, tournament=0):
    Adds a player to the tournament database.
     Args:
      name: the player's full name (need not be unique).
     Returns:
      "OK" if correctly inserted
      "ERROR" Database error description
    
    
def registerTournament(tournament_name):
    Adds a torunament to the tournament database.
     Args:
      name: the tourament name (need not be unique).
     Returns:
      "ERROR" Database error description


def reportMatch(winner, loser, tie_result=False):
   Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tournament: Id of the tournament the match belongs to
    Returns:
      "OK" if correctly inserted
      "ERROR" Database error description
      "ERROR - Game duplicated" If the game is already in the database
      "ERROR Players not in the same tournament"
    """
    
    
def checkExistanceOfMatch(winner, loser):
    Checks if a particular game from a particular tournament is already in
    the database
       Args:
        Winner and loser: The ID of the participants of the match 
       Returns:
        False if the game is not present
        True if the game is already present


def check_Players_in_tournament(winner, loser):
    Checks if a couple of players are in the same tournament and can play a 
    match
       Args:
        Winner and loser: Ids of the players
       Returns:
        False if the game is not present
        True if the game is already present


def playerStandings(tournament=0):
    Returns a list of the players and their win records, sorted by wins.
    The tournament ID =  0 is reserved for all tournaments
    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.
    Args:
      tournament: tournament_ID 
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played


def swissPairings(tournament=0):
    Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    Args:
      tournament: tournament_ID 
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
 

    