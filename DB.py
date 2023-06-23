import sqlite3
conn = sqlite3.connect('game_reviews_indie_reddit.sqlite')
c = conn.cursor()
import pandas as pd


# Execute a SELECT query and return the results as a pandas DataFrame.
df = pd.read_sql_query('SELECT * FROM Comments', conn)

df.to_csv('comments_indie_reddit.csv', index=False, encoding='utf-8-sig')


import sqlite3

# Connect to the first database.
conn1 = sqlite3.connect('game_reviews_indie.sqlite')
cur1 = conn1.cursor()

# Connect to the second database.
conn2 = sqlite3.connect('game_reviews_indie_reddit.sqlite')
cur2 = conn2.cursor()

# Create a new database and a cursor for it.
new_db = sqlite3.connect('new_db.sqlite')
new_cur = new_db.cursor()

# Assume 'game_reviews_indie' and 'game_reviews_indie_reddit' have the same schema.
# Create a new table in the new database.
#new_cur.execute('''
#    CREATE TABLE game_reviews_merged
#    (game TEXT, comment TEXT)
#''')

# Insert the data from the first and the second databases into the new one.
for cur, table in [(cur1, "comments"), (cur2, "comments")]:
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    new_db.executemany("INSERT INTO game_reviews_merged VALUES (?, ?)", rows)

# Commit the changes and close the connections.
new_db.commit()
conn1.close()
conn2.close()
new_db.close()
