#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


result = []


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    conn = connect()
    db_cursor = conn.cursor()
    query = "delete from matches;"
    db_cursor.execute(query)
    conn.commit()
    conn.close()
    # """Remove all the match records from the database."""


def deletePlayers():
    conn = connect()
    db_cursor = conn.cursor()
    query = "delete from players;"
    db_cursor.execute(query)
    conn.commit()
    conn.close()
    # """Remove all the player records from the database."""


def countPlayers():
    conn = connect()
    db_cursor = conn.cursor()
    query = "select count(*) from Players;"
    db_cursor.execute(query)
    return db_cursor.fetchone()[0]
    conn.close()

    # """Returns the number of players currently registered."""


def countMatches():
    conn = connect()
    db_cursor = conn.cursor()
    query = "select count(*) from Matches;"
    db_cursor.execute(query)
    return db_cursor.fetchone()[0]
    conn.close()


def registerPlayer(name):
    conn = connect()
    db_cursor = conn.cursor()
    query = "insert into players (name) values (%s);"
    db_cursor.execute(query, (name,))
    conn.commit()
    conn.close()


def playerStandings():
    data = []
    conn = connect()
    db_cursor = conn.cursor()

    if countMatches() == 0:
        query = "select players.id, players.name, 0 as wintotal,0 as matches_played from players order by wintotal desc;"
        # query = "select players.id, players.name from players order by id desc;"
    elif countMatches() >= 1:
        query = "select * from standings;"

    db_cursor.execute(query)

    for row in db_cursor.fetchall():
        data.append(row)

    conn.close()
    return data
    # """Returns a list of the players and their win records, sorted by wins.

    # The first entry in the list should be the player in first place, or a player
    # tied for first place if there is currently a tie.

    # Returns:
    # A list of tuples, each of which contains (id, name, wins, matches):
    # id: the player's unique id (assigned by the database)
    #name: the player's full name (as registered)
    #wins: the number of matches the player has won
    #matches: the number of matches the player has played


def reportMatch(winner, loser):
    conn = connect()
    db_cursor = conn.cursor()
    count = countMatches()
    query = "insert into matches (id, winner, loser) values (%s,%s,%s);"
    count += 1
    db_cursor.execute(query, (str(count), winner, loser))
    conn.commit()
    conn.close()
    # """Records the outcome of a single match between two players.


# Args:
# winner:  the id number of the player who won
# loser:  the id number of the player who lost

def swissPairings():
    result = []
    standings = playerStandings()

    i = 0

    while i < len(standings):
        result.append((standings[i][0], standings[i][1], standings[i + 1][0], standings[i + 1][1]))
        i += 2

    return result
    # """Returns a list of pairs of players for the next round of a match.

    # Assuming that there are an even number of players registered, each player
    # appears exactly once in the pairings.  Each player is paired with another
    # player with an equal or nearly-equal win record, that is, a player adjacent
    #to him or her in the standings.

    #Returns:
    #A list of tuples, each of which contains (id1, name1, id2, name2)
    # id1: the first player's unique id
    #name1: the first player's name
    #id2: the second player's unique id
    #name2: the second player's name


def createRandomMatches(num_matches):
    # method use during test and would not be use for project
    num_players = int(countPlayers())
    id = []
    name = []
    winner_id = 1
    loser_id = 2
    winner_name = "A"
    loser_name = "B"
    conn = connect()
    db_cursor = conn.cursor()
    query = "select * from Players;"
    db_cursor.execute(query)
    for (i, n) in db_cursor.fetchall():
        id.append(i)
        name.append(n)

    for i in xrange(num_players / 2):
        print 'match %s' % (i + 1)
        player_1index = random.randint(0, countPlayers() - 1)
        player_2index = random.randint(0, countPlayers() - 1)

        if player_2index == player_1index:
            player_2index = (player_1index + 1) % num_players
        elif player_1index > player_2index:
            winner_id = id[i]
            loser_id = id[i + 1]
        else:
            loser_id = id[i]
            winner_id = id[i + 1]

        reportMatch(winner_id, loser_id)
        print "%s (id=%s) beat %s (id=%s)" % (winner_name, winner_id, loser_name, loser_id)
    conn.close()
