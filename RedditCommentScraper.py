import sqlite3
import praw
conn= sqlite3.connect('game_reviews_indie_reddit.sqlite')
c= conn.cursor()
#c.execute('''CREATE TABLE comments (game Text, comment Text)''')
conn.commit()
   
reddit = praw.Reddit(client_id='HQRw-RfjSTfl-i5pBCazzw',
                     client_secret='SXqozGUqYS62LtZ2M93jPR91EJrybA',
                     user_agent='my user agent')
subreddit = reddit.subreddit('ShouldIbuythisgame')
posts=[]
with open('indieGameList.txt','r') as f:
    for line in f:
        search_query = "should I buy "+line.strip()
        search_results = subreddit.search(search_query, limit=1)  # Get the top 10 results.
        for post in search_results:  # Loop over the ListingGenerator.
            posts.append(post) 
            print(f"Title: {post.title}")
            
            post.comments.replace_more(limit=0)  # Resolve 'MoreComments' instances.
            top_comments = post.comments.list()[:]  # Get the top 5 comments.
            
            for comment in top_comments:
                 c.execute('''
            INSERT INTO comments (game, comment) 
            VALUES (?, ?)
        ''', (line.strip(), comment.body))
conn.commit()
conn.close()