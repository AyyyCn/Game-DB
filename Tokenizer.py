
"""import nltk
nltk.download('punkt')  # Re-download punkt
nltk.download('wordnet')  # Ensure WordNet works
nltk.download('stopwords')  # Ensure stopwords are available
"""

import nltk
import sqlite3
import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
# Initialize tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Connect to the SQLite database
conn = sqlite3.connect('big_games_reviews.sqlite')

# Load the comments table into a DataFrame
df = pd.read_sql_query("SELECT * FROM comments", conn)

# Preprocessing function: clean, tokenize, and lemmatize
def clean_and_tokenize(comment):
    tokens = word_tokenize(comment.lower())  # Lowercasing and tokenization
    tokens = [word for word in tokens if word not in stop_words and word not in string.punctuation]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]  # Lemmatize words
    return " ".join(tokens)  # Convert tokens back into a single string

# Apply tokenization to comments
df['tokenized_comment'] = df['comment'].apply(clean_and_tokenize)

# Write results into a new table `comments_Tokenized`
df[['game', 'tokenized_comment']].to_sql('comments_Tokenized', conn, if_exists='replace', index=False)

# Close the database connection
conn.close()

print("Tokenized comments successfully written to 'comments_Tokenized' table.")
