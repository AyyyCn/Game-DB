import spacy
import pandas as pd

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# Expanded aspect categories and keywords
aspect_keywords = {
    "graphics": ["graphics", "visuals", "design", "animation", "textures", "art", "lighting", "shadows", "rendering", "aesthetics"],
    "gameplay": ["gameplay", "mechanics", "controls", "combat", "difficulty", "level design", "progression", "interaction", "customization"],
    "story": ["story", "plot", "narrative", "dialogue", "writing", "characters", "lore", "world-building", "quest", "cutscenes"],
    "sound": ["sound", "music", "audio", "soundtrack", "voice acting", "effects", "ambience", "immersion"],
    "performance": ["performance", "fps", "loading", "bugs", "crashes", "optimization", "lag", "stuttering", "patches"],
    "multiplayer": ["multiplayer", "online", "matchmaking", "servers", "ping", "co-op", "PvP", "connectivity"],
    "replayability": ["replayability", "content", "endgame", "challenges", "mods", "achievements", "side quests"],
    "monetization": ["monetization", "microtransactions", "DLC", "loot boxes", "pricing", "season pass", "value"]
}

# Function to map entities to aspects
def extract_aspects(comment):
    doc = nlp(comment)
    aspects = {}
    for token in doc:
        for aspect, keywords in aspect_keywords.items():
            if any(keyword in token.text.lower() for keyword in keywords):
                if aspect not in aspects:
                    aspects[aspect] = []
                aspects[aspect].append(token.text)
    return aspects

# Load comments
df = pd.read_csv("bert/train.csv")  # Example file
# Ensure all text fields are strings and handle missing values
df['text'] = df['text'].astype(str).fillna('')

# Extract aspects
df['aspects'] = df['text'].apply(extract_aspects)
# Save extracted aspects to a new file
df.to_csv("aspect_analysis/aspects_extracted.csv", index=False)
print("Aspects extracted and saved to 'aspect_analysis/aspects_extracted.csv'")
