from googleapiclient.discovery import build
import pandas as pd
import sqlite3
conn = sqlite3.connect('game_reviews.sqlite')

c= conn.cursor()
#c.execute('''CREATE TABLE comments (game Text, comment Text)''')
conn.commit()
conn.close()
# Replace with your YouTube Data API key.
api_key = "AIzaSyCWVno9BT4udY9t2W1nwdkBSIWMLQT4ifU"

youtube = build('youtube', 'v3', developerKey=api_key)

def get_comments(video_id,game_name, max_results=200):
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results, 
        textFormat="plainText"
    )
    response = request.execute()
    conn = sqlite3.connect('game_reviews.sqlite')
    c = conn.cursor()

    for item in response["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        c.execute('''
            INSERT INTO comments (game, comment) 
            VALUES (?, ?)
        ''', (game_name, comment))
    conn.commit()
    conn.close()

def get_videos(game_name, max_results=4):
    request = youtube.search().list(
        q=f"{game_name} game review",
        part="id,snippet",
        maxResults=max_results,
        type="video"
    )
    response = request.execute()

    for item in response["items"]:
        print(f'Title: {item["snippet"]["title"]}, Video ID: {item["id"]["videoId"]}')
        get_comments(item["id"]["videoId"],game_name)
        
pd = pd.read_csv('final_data.csv')

for i in pd['Title']:
    get_videos(i)