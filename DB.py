import sqlite3
conn = sqlite3.connect('game_reviews.sqlite')
c = conn.cursor()
import pandas as pd


# Execute a SELECT query and return the results as a pandas DataFrame.
df = pd.read_sql_query('SELECT * FROM Comments', conn)

df.to_csv('comments.csv', index=False, encoding='utf-8-sig')
