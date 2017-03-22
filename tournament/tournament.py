#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import types

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches(tournament_id=None):
    """Remove all the match records from the database for given tournament or all.
        args: tournament_id (optional), int
            if tournament_id is not given all match records are deleted
            if tournament_id is given all matches for given tournament are deleted

        Returns boolean
            False = Invalid argument or some exception thrown in DB
            True = matches deleted according to arg supplied (or not supplied)
    """
    # Validate input
    if not validate_input(tournament_id, [types.NoneType, types.IntType], True):
        return False
    # Connect to database and setup cursor
    conn = connect()
    c = conn.cursor()

    # Setup query str and try to execute query or throw exception, close connection
    try:
        if tournament_id:
            query_str = "DELETE FROM matches where tournament_id = %s;"
            c.execute(query_str, (tournament_id, ))
        else:
            query_str = "TRUNCATE TABLE matches;"
            c.execute(query_str)
        conn.commit()
        c.close()
        conn.close()
    except psycopg2.Error as e:
        # print e # Uncomment for degbugging
        return False
    else:
        return True


def deletePlayers(player_id=None):
    """Remove all or specified player(s) records from the database.
        args: player_id (optional), int
            if player_id is not given all player records are deleted
            if player_id is given player is removed

        Returns boolean
            False = Invalid argument or some exception thrown in DB
            True = matches deleted according to arg supplied (or not supplied)
    """
    if not validate_input(player_id, [types.NoneType, types.IntType], True):
        return False

    # Connect to database and setup cursor
    conn = connect()
    c = conn.cursor()
    # Setup query str and try to execute query or throw exception, close connection
    try:
        if player_id:
            query_str = "DELETE FROM tournament_participants WHERE player_id = %s;"
            c.execute(query_str, (player_id,))
            query_str = "DELETE FROM players WHERE player_id = %s;"
            c.execute(query_str, (player_id, ))
        else:
            query_str = "DELETE FROM tournament_participants;"
            c.execute(query_str)
            query_str = "DELETE FROM players;"
            c.execute(query_str)
        conn.commit()
        c.close()
        conn.close()
    except psycopg2.Error as e:
        # print e # Uncomment for degbugging
        return False
    else:
        return True


def deleteTournament(tournament_id=None):
    """Remove all or specified player(s) records from the database.
        args: player_id (optional), int
            if player_id is not given all player records are deleted
            if player_id is given player is removed

        Returns boolean
            False = Invalid argument or some exception thrown in DB
            True = matches deleted according to arg supplied (or not supplied)
    """
    if not validate_input(tournament_id, [types.NoneType, types.IntType], True):
        return False

    # Connect to database and setup cursor
    conn = connect()
    c = conn.cursor()
    # Setup query str and try to execute query or throw exception, close connection
    try:
        if tournament_id:
            query_str = "DELETE FROM tournament WHERE tournament_id = %s;"
            c.execute(query_str, (tournament_id, ))
            query_str = "DELETE FROM tournament_participants WHERE tournament_id = %s;"
            c.execute(query_str, (tournament_id,))
        else:
            query_str = "DELETE FROM tournament;"
            c.execute(query_str)
            query_str = "DELETE FROM tournament_participants;"
            c.execute(query_str)
        conn.commit()
        c.close()
        conn.close()
    except psycopg2.Error as e:
        # print e # Uncomment for degbugging
        return False
    else:
        return True


def countPlayers(tournament_id=None):
    """Returns the number of players currently registered. or if tournament_id given count
        number of players registered for given tournament

        args:
            tournament_ID, int, Optional, default=None
        Returns:
            Int, number of register players
            False on invalid input or DB exception
    """
    # Validate input
    if not validate_input(tournament_id, [types.NoneType, types.IntType], True):
        return False

    # Connect to database and setup cursor
    conn = connect()
    c = conn.cursor()
    # Setup query str and try to execute query or throw exception, close connection, structure return
    try:
        if tournament_id:
            query_str = "SELECT count(player_id) FROM tournament_participants WHERE tournament_id = %s;"
            c.execute(query_str, (tournament_id, ))
        else:
            query_str = "SELECT count(player_id) FROM players;"
            c.execute(query_str)
        result = c.fetchone()
        conn.commit()
        c.close()
        conn.close()
    except psycopg2.Error as e:
        # print e # Uncomment for degbugging
        return False
    else:
        return int(result[0])

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

  
    Args:
      name: the player's full name (need not be unique).
    Returns:
        player_id if insert succeded
        False if input not text or db throws exception
    """

    #validate input
    if not validate_input(name, [types.StringType], True):
        return False

    conn = connect()
    c = conn.cursor()

    # setup query_string and try to execute, close connection
    try:
        c.execute("INSERT INTO players (player_name) VALUES (%s);", (name, ))
        c.execute("SELECT currval(pg_get_serial_sequence('players', 'player_id'));")
        player_id = c.fetchone()
        conn.commit()
        c.close()
        conn.close()
    except psycopg2.Error as e:
        # print e # Uncomment for degbugging
        return False
    else:
        return int(player_id[0])

def registerTournament(name):
    """ Adds a tournament

        Args:
            name: tournament name as string
        Returns:
            the tournament ID as an int or False if error
    """
    #validate input
    if not validate_input(name, [types.StringType], True):
        return False

    # Connect to db
    conn = connect()
    c = conn.cursor()
    # setup query_string and try to execute, close connection
    try:
        c.execute("INSERT INTO tournament (tournament_name) VALUES (%s);", (name, ))
        c.execute("SELECT currval(pg_get_serial_sequence('tournament', 'tournament_id'));")
        tournament_id = c.fetchone()
        conn.commit()
        c.close()
        conn.close()
    except psycopg2.Error as e:
        # print e # Uncomment for degbugging
        return False
    else:
        return int(tournament_id[0])


def registerPlayerInTournament(player_id, tournament_id):
    """Adds a given player to a given tournament in tournament_participant table

        Args:
            player_id, int
            tournament_id, int
        Returns:
            True if success
            False if DB exception or input invalid
    """
    if not (validate_input(player_id, [types.IntType], True) or validate_input(tournament_id, [types.IntType], True)):
        return False
    # Connect to DB and setup cursor
    conn = connect()
    c = conn.cursor()

    # setup query_string and try to execute, close connection
    try:
        c.execute("INSERT INTO tournament_participants (player_id, tournament_id) VALUES (%s, %s);",
                  (player_id, tournament_id, ))
        conn.commit()
        c.close()
        conn.close()
    except psycopg2.Error as e:
        # print e # Uncomment for degbugging
        return False
    else:
        return True


def playerStandings(tournament_id):
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
    if not validate_input(tournament_id, [types.IntType], True):
        return False
    # Connect to DB and setup cursor
    conn = connect()
    c = conn.cursor()
    # setup query_string and try to execute, close connection
    try:
        c.execute("SELECT \
                    player_id, \
                    player_name, \
                    wins, \
                    matches as matches \
                   FROM matches_summary \
                   WHERE tournament_id = %s \
                   ORDER BY wins DESC;", (tournament_id, ))
        query_result = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
    except psycopg2.Error as e:
        # print e # Uncomment for degbugging
        return False
    else:
        # Structure result and return
        func_result = []
        for row in query_result:
            func_result.append((row[0], row[1], int(row[2]), int(row[3])))
        return func_result


def reportMatch(winner, loser, tournament_id):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tournament_id: the id number of the tournament in which the match was played
    Returns:
        True if insert succeded
        False if insert failed or input data invalid
    """
    if not validate_input(winner, [types.IntType], True):
        return False
    if not validate_input(loser, [types.IntType], True):
        return False
    if not validate_input(tournament_id, [types.IntType], True):
        return False
    # connect to db
    conn = connect()
    c = conn.cursor()

    # update matches entry with result in matches table
    try:
        c.execute("INSERT INTO matches (tournament_id, winner, loser) VALUES (%s, %s, %s)",
                  (tournament_id, winner, loser, ))
        conn.commit()
        c.close()
        conn.close()
    except psycopg2.Error as e:
        # print e # Uncomment for degbugging
        return False
    else:
        return True
 
def swissPairings(tournament_id):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Args:
        tournament_id: Id of tournament being played
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    if not validate_input(tournament_id, [types.IntType], True):
        return False
        # Connect to DB and setup cursor
    conn = connect()
    c = conn.cursor()
    # setup query_string and try to execute, close connection
    try:
        c.execute("SELECT \
                       player_id, \
                       player_name \
                      FROM matches_summary \
                      WHERE tournament_id = %s \
                      ORDER BY wins DESC;", (tournament_id,))
        query_result = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
    except psycopg2.Error as e:
        # print e # Uncomment for degbugging
        return False
    else:
        # Structure result and return, assumes even number of tournament participants
        # loop through query result ant create tuples of even and odd index pairs and append to list
        func_result = []
        for i, row in enumerate(query_result):
            if (i % 2) == 0:
                res_tuple = (row[0], row[1])
            else:
                res_tuple += row[0], row[1]
                func_result.append(res_tuple)
        return func_result


def validate_input(input, expected_values, type_test=False):
    """Returns Boolean
        args:
            input: input value to test
            expected_values: list of expected, accepted values
            type_test: optional, default=False, if true tests types not values
    """
    if type_test:
        if type(input) in expected_values:
            return True
    else:
        if input in expected_values:
            return True
    return False

## TODO
# 1. write unit tests
# 3. make all funcs pass own unit tests
# 4. modify tournament_test.py

def test_register_player():
    u =registerPlayer("Calle")
    d = registerPlayer("Nissse")
    if u and d:
        print "user " + u + " and " + d + " were created"
    else:
        "Failed to create users"

def test_delete_player():
    a = deletePlayers()
    if a:
        print "Delete users success"
    else:
        print "failed to delete users"


