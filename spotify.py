import sqlite3
import os
import requests
import secret

playlist_id = '6UeSakyzhiEt4NB3UAd6NQ'
access_token = secret.spotify_token
def set_up_database():
    """
    This function does not take in any parameters. It 
    establishes a connection to data.db. It then creates 
    two tables (artist and topTracks) if they do not already 
    exist. The connection and corresponding cursor is returned.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/data.db')
    cur = conn.cursor()
    # Create 'artist' table
    cur.execute("""CREATE TABLE IF NOT EXISTS artist 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   name TEXT UNIQUE)""")

    # Create 'topTracks' table with a foreign key referencing 'artist' table
    cur.execute("""CREATE TABLE IF NOT EXISTS topTracks 
                   (song_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   title TEXT, 
                   popularity INTEGER, 
                   artist_id INTEGER, 
                   FOREIGN KEY(artist_id) REFERENCES artist(id))""")
    return cur, conn

def get_data():
    """
    This function does not take in any parameters. It
    calls the Spotify API to get data for the tracks in 
    Billboard's Top 100 Hits. The function returns a list 
    containing information for each track.
    """
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    playlist_data = response.json()['tracks']['items']
    return playlist_data
    
def update_database(cur, conn, data):
    """
    This function takes in the database cursor, database 
    connection, and playlist data. It inserts information 
    for 25 songs at a time into the topTracks table and 
    artist table. The function does not return anything
    """
    cur.execute("SELECT COUNT(*) FROM topTracks")
    size = cur.fetchone()[0]
    for i in range(size, size + 25):
        title = data[i]['track']['name']
        popularity = data[i]['track']['popularity']
        artist = data[i]['track']['artists'][0]['name']
        cur.execute(
            "INSERT OR IGNORE INTO artist (name) VALUES (?)", (artist,)
        )
        cur.execute("SELECT id FROM artist WHERE name = ?", (artist,))
        artist_id = cur.fetchone()[0]
        cur.execute("""INSERT OR IGNORE INTO topTracks 
                    (title, popularity, artist_id) VALUES (?, ?, ?)""", 
                    (title, popularity, artist_id))
        conn.commit()

def main():
    cur, conn = set_up_database()
    data = get_data()
    update_database(cur, conn, data)

if __name__ == "__main__":
    main()