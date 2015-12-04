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
    status = "OK"
    db = connect()
    cur = db.cursor()

    columns_str = ", ".join([str(s) for s in column_data.keys()])
    args_str = ", ".join(["%(" + str(s) + ")s" for s in column_data.keys()])

# Format the query to be executed
    query = "INSERT INTO {} ({}) VALUES ({})".format(table, columns_str,
                                                     args_str)
    print query 
    try:
        cur.execute(query, column_data)
    except psycopg2.Error as error:
        status = error.pgerror

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
        cur.execute("SELECT count(player_ID) FROM players")
        results = cur.fetchall()
        results = results[0][0]
    except psycopg2.Error as error:
        results = 'ERROR - Problems with the database'

    close_connection(db)
    return (results)


def registerPlayer(players_name, tournament=0):
    """Adds a player to the tournament database.
     Args:
      name: the player's full name (need not be unique).
     Returns:
      "OK" if correctly inserted
      "ERROR" Database error description
    """
    return registerMultipleData("players", name=players_name,
                                tournament_ID=tournament)


def registerTournament(tournament_name):
    """Adds a torunament to the tournament database.
     Args:
      name: the tourament name (need not be unique).
     Returns:
      "ERROR" Database error description
    """
    return registerMultipleData("tournaments", name=tournament_name)


def reportMatch(winner, loser, tie_result=False):
    """Records the outcome of a single match between two players.

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

    if not(check_Players_in_tournament(winner, loser)):
        return "ERROR Players not in the same tournament"

    if (checkExistanceOfMatch(winner, loser)):
        return "ERROR - Game duplicated"

    return registerMultipleData("matches", winner_ID=winner,
                                loser_ID=loser, tie=tie_result)


def checkExistanceOfMatch(winner, loser):
    """Checks if a particular game from a particular tournament is already in
       the database
       Args:
        Winner and loser: The ID of the participants of the match 
       Returns:
        False if the game is not present
        True if the game is already present
    """
# Check the existance of the game in the database, disregard of the results
    db = connect()
    cur = db.cursor()
    query = "SELECT count(*) FROM matches WHERE ((winner_ID = {} AND \
    loser_ID = {}) OR (winner_ID = {} AND loser_ID = {}))"\
    .format(winner, loser, loser, winner)

    cur.execute(query)
    results = cur.fetchall()
    close_connection(db)

    if results[0][0]:
        return True
    else:
        return False


def check_Players_in_tournament(winner, loser):
    """Checks if a couple of players are in the same tournament and can play a 
    match
       Args:
        Winner and loser: Ids of the players
       Returns:
        False if the game is not present
        True if the game is already present
    """
# Check the existance of the game in the database, disregard of the results
    db = connect()
    cur = db.cursor()
    query = ("SELECT tournament_ID FROM players WHERE player_ID = %s \
    OR player_ID = %s")

    cur.execute(query, (winner, loser))
    results = cur.fetchall()
    close_connection(db)

    [t1, t2] = [row[0] for row in results]

    if t1 == t2:
        return True
    else:
        return False


def playerStandings(tournament=0):
    """Returns a list of the players and their win records, sorted by wins.
    The tournament ID =  0 is reserved for all tournaments
    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.
    Args:
      The tournament_ID
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cur = db.cursor()
    # Check if the petition is from an specific tournament or for all players
    if(tournament):
        query = "SELECT * FROM standings WHERE games.tournament_ID = {}"\
        .format(tournament)

    else:
        query = "SELECT * FROM standings;"

    cur.execute(query)
    results = cur.fetchall()
    close_connection(db)

    return [(row[0], row[1], row[2], row[3]) for row in results]


def swissPairings(tournament=0):
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
    players = playerStandings(tournament)
    results = [(i, n) for (i, n, w, m) in players]
    results = iter(results)

    return [(x[0], x[1], y[0], y[1]) for x, y in zip(results, results)]
    