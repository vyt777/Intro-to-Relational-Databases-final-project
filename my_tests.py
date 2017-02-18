from tournament import *

number = playerStandings()


print number

# rating real number?
#
#
#
#
conn = connect()
    c = conn.cursor()
    query = "INSERT INTO player_stats (name, matches, wins, rating) VALUES (%s, '0', '0', '0');"
    c.execute(query, (name,))
    conn.commit()
    conn.close()