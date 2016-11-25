#
# Database access functions for the web forum.
#

import time
import psycopg2
import bleach

## Database connection
# DB = psycopg2.connect("dbname=forum")

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    conn = psycopg2.connect("dbname=forum")
    cursor = conn.cursor()
    cursor.execute(
        "select * from posts"
    )
    DB = cursor.fetchall()

    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
    posts.sort(key=lambda row: row['time'], reverse=True)

    conn.close()
    
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    conn = psycopg2.connect("dbname=forum")
    cursor = conn.cursor()

    t = time.strftime('%c', time.localtime())
    cursor.execute(
        "insert into posts values (%s, %s)",(bleach.clean(content), t)
    )
    conn.commit()

    conn.close()
