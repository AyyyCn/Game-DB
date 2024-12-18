# Load necessary libraries
import pandas as pd
from transformers import pipeline

# Load extracted aspects
df = pd.read_csv("aspect_analysis/aspects_extracted.csv")
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased")

# Function to associate sentiment with aspects
def analyze_aspect_sentiments(row):
    aspect_sentiments = {}
    for aspect, terms in eval(row['aspects']).items():  # Convert stringified dict to actual dict
        combined_text = " ".join(terms)[:512]  # Truncate to maximum allowed tokens
        sentiment = sentiment_analyzer(combined_text)[0]  # Predict sentiment
        aspect_sentiments[aspect] = sentiment['label']  # Example: 'POSITIVE', 'NEGATIVE', etc.
    return aspect_sentiments

# Apply sentiment analysis to aspects
df['aspect_sentiments'] = df.apply(analyze_aspect_sentiments, axis=1)

# Save results
df.to_csv("aspect_analysis/aspect_sentiments.csv", index=False)
print("Aspect sentiments saved to 'aspect_analysis/aspect_sentiments.csv'")
