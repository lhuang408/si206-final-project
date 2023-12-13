import sqlite3
import os
import requests
import secret
def set_up_database():
    """
    This function does not take in any parameters. It 
    establishes a connection to data.db. It then a words 
    table if it does not already exist. The connection and 
    corresponding cursor is returned.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/data.db')
    cur = conn.cursor()
    # Create 'words' table
    cur.execute("""CREATE TABLE IF NOT EXISTS words 
                   (song_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   score FLOAT)""")
    return cur, conn

def update_database(cur, conn):
    """
    This function takes in the database cursor and database 
    connection. It grabs 25 song titles at a time and calls 
    the TwinWords API to determine the sentiment. This is added 
    into the words table. The function does not return anything.
    """
    cur.execute("SELECT COUNT(*) FROM words")
    size = cur.fetchone()[0]
    for i in range(size + 1, size + 26):
        cur.execute("SELECT title FROM topTracks WHERE song_id = ?", (i,))
        title = cur.fetchone()[0]
        url = "https://twinword-twinword-bundle-v1.p.rapidapi.com/sentiment_analyze/"
        querystring = {"text":title}
        headers = {
            "X-RapidAPI-Key": secret.words_token,
            "X-RapidAPI-Host": "twinword-twinword-bundle-v1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        score = response.json()['score']
        cur.execute("""INSERT INTO words (score) 
                    VALUES (?)""", (float(score),))
        conn.commit()

def main():
    cur, conn = set_up_database()
    update_database(cur, conn)

if __name__ == "__main__":
    main()