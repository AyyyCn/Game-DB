import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import sqlite3
import emoji

nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_game_title(title):
    """Convert a game title into a 'clean' form that can be recognized in text."""
    return title.lower().replace(' ', '_')

def clean_text(text, game_title):
    """Clean text data, preserving game title."""
    cleaned_title = clean_game_title(game_title)
    
    # Replace game title in the text with its 'cleaned' version.
    text = text.replace(game_title, cleaned_title)
    
    text = text.lower()  # Convert to lowercase.
    text = re.sub('@\w+', '', text)  # Remove mentions
    text = emoji.demojize(text)  # Convert emojis to text.
    text = re.sub('<.*?>', '', text)  # Remove HTML tags.
    text = re.sub('[^\w\s]', '', text)  # Remove punctuation.
    text = re.sub('\n', '', text)  # Remove newlines.
    text = re.sub('\d+', '', text)  # Remove numbers.
    
    # Remove stopwords, but keep cleaned game title.
    text = ' '.join(word for word in text.split() if word not in stop_words or word == cleaned_title)
    
    # Lemmatize words, but keep cleaned game title.
    text = ' '.join(lemmatizer.lemmatize(word) if word != cleaned_title else word for word in text.split())
    
    return text


conn = sqlite3.connect('new_db.sqlite')
c = conn.cursor()

# Select all game and comment pairs from the database.
c.execute("SELECT game, comment FROM game_reviews_merged")
rows = c.fetchall()

# Loop over each row and clean the comments.
for row in rows:
    game_title, comment = row
    cleaned_comment = clean_text(comment, game_title)

    # Update the comment in the database.
    c.execute("UPDATE game_reviews_merged SET comment = ? WHERE game = ? AND comment = ?", (cleaned_comment, game_title, comment))

conn.commit()
conn.close()