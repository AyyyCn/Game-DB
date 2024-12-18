import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load aspect sentiment data
df = pd.read_csv("aspect_analysis/aspect_sentiments.csv")

# Convert stringified dictionaries back to actual dictionaries
df['aspect_sentiments'] = df['aspect_sentiments'].apply(eval)

# Map numeric labels to clearer sentiment names
sentiment_mapping = {"LABEL_0": "Negative", "LABEL_1": "Positive"}

# Function to aggregate sentiments for each aspect
def aggregate_sentiments(data):
    aspect_summary = {}
    for sentiments in data:
        for aspect, sentiment in sentiments.items():
            sentiment_label = sentiment_mapping.get(sentiment, sentiment)
            if aspect not in aspect_summary:
                aspect_summary[aspect] = Counter()
            aspect_summary[aspect][sentiment_label] += 1
    return aspect_summary

# Aggregate sentiment data
aspect_summary = aggregate_sentiments(df['aspect_sentiments'])

# Plot sentiment distribution for each aspect
for aspect, sentiment_counts in aspect_summary.items():
    labels = list(sentiment_counts.keys())
    values = list(sentiment_counts.values())

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=['red', 'green'])
    plt.title(f"Sentiment Distribution for {aspect.capitalize()}")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.show()
