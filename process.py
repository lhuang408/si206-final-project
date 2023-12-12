import sqlite3
import os
import json

def set_up_database():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/data.db')
    cur = conn.cursor()
    return cur

def write_json(filename, dict):
    '''
    Encodes dict into JSON format and writes
    the JSON to filename to save the search results

    Parameters
    ----------
    filename: string
        the name of the file to write a cache to
    
    dict: cache dictionary

    Returns
    -------
    None
        does not return anything
    '''  
    with open(filename, 'w') as f:
        f.write(json.dumps(dict, indent=4))

def category_freq(cur):
    cur.execute("SELECT score FROM words")
    output = cur.fetchall()
    title_d = {}
    for item in output:
        score = item[0]
        if score < 0:
            title_d['negative'] = title_d.get('negative', 0) + 1
        elif score == 0:
            title_d['neutral'] = title_d.get('neutral', 0) + 1
        else:
            title_d['positive'] = title_d.get('positive', 0) + 1
    write_json('category_freq.json', title_d)

   
def artist_freq(cur):
    cur.execute("""SELECT artist.name
                   FROM topTracks
                   JOIN artist ON 
                   topTracks.artist_id = artist.id""")
    output = cur.fetchall()
    artist_d = {}
    for item in output:
        name = item[0]
        artist_d[name] = artist_d.get(name, 0) + 1
    artist_d = {k:v for k, v in artist_d.items() if v > 3}
    write_json('artist_freq.json', artist_d)


def avg_pop(cur):
    d = {}
    cur.execute("""SELECT topTracks.popularity
                   FROM topTracks
                   JOIN words ON words.song_id = topTracks.song_id
                   WHERE words.score < 0""")
    output = cur.fetchall()
    total = 0
    for item in output:
        total += item[0]
    negative_avg = total / len(output)
    d['negative'] = negative_avg

    cur.execute("""SELECT topTracks.popularity
                   FROM topTracks
                   JOIN words ON words.song_id = topTracks.song_id
                   WHERE words.score = 0""")
    output = cur.fetchall()
    total = 0
    for item in output:
        total += item[0]
    neutral_avg = total / len(output)
    d['neutral'] = neutral_avg

    cur.execute("""SELECT topTracks.popularity
                   FROM topTracks
                   JOIN words ON words.song_id = topTracks.song_id
                   WHERE words.score > 0""")
    output = cur.fetchall()
    total = 0
    for item in output:
        total += item[0]
    positive_avg = total / len(output)
    d['positive'] = positive_avg
    write_json('avg_pop.json', d)

def popularity_and_sentiment(cur):
    cur.execute("""SELECT topTracks.title, topTracks.popularity, words.score
                   FROM topTracks
                   JOIN words ON words.song_id = topTracks.song_id""")
    output = cur.fetchall()
    d = []
    for item in output:
        d.append({"title": item[0], "popularity": item[1], "sentiment": item[2]})
    write_json('popularity_and_sentiment.json', d)


        

def main():
    cur = set_up_database()
    category_freq(cur)
    artist_freq(cur)
    avg_pop(cur)
    popularity_and_sentiment(cur)


if __name__ == "__main__":
    main()