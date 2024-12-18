"""Cleans and tokenizes comments.
Splits data into training and validation sets."""

import pandas as pd
from sklearn.model_selection import train_test_split
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sqlite3
import nltk

nltk.download('vader_lexicon')

# Connect to the database
conn = sqlite3.connect('big_games_reviews.sqlite')
df = pd.read_sql_query("SELECT game, comment FROM comments", conn)

# Drop null comments
df = df.dropna(subset=['comment'])

# Initialize VADER
sid = SentimentIntensityAnalyzer()

# Function to assign labels
def get_sentiment(comment):
    score = sid.polarity_scores(comment)['compound']
    if score > 0.05:
        return 'positive'
    elif score < -0.05:
        return 'negative'
    else:
        return 'neutral'

# Add sentiment labels
df['label'] = df['comment'].apply(get_sentiment)

# Train-Test Split
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df['comment'], df['label'], test_size=0.2, random_state=42
)

# Save to files
train = pd.DataFrame({'text': train_texts, 'label': train_labels})
val = pd.DataFrame({'text': val_texts, 'label': val_labels})

train.to_csv('bert/train.csv', index=False)
val.to_csv('bert/val.csv', index=False)

print("Data preprocessing completed with sentiment labels added.")
