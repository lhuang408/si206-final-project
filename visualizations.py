import json
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def read_data_from_file(filename):
    """
    Reads data from a file with the given filename. 
    It takes in a filename and returns parsed JSON 
    data from the file.
    """
    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    return json_data

def avg_pop():
    """
    This function does not take in any parameters. 
    It reads data from avg_pop.json and creates a 
    bar chart to visualize the average popularity of 
    songs in each sentiment category. The function 
    does not return anything.
    """
    data = read_data_from_file('avg_pop.json')
    sentiment = []
    popularity = []
    for item in data.items():
        sentiment.append(item[0])
        popularity.append(item[1])
    plt.figure()
    bars = plt.bar(sentiment, popularity)
    bars[0].set_color('lightcoral')
    bars[1].set_color('lemonchiffon')
    bars[2].set_color('skyblue')
    plt.title('Average Popularity Score for each Sentiment Category')
    plt.xlabel('Sentiment')
    plt.ylabel('Average Popularity Score')
    plt.savefig('avg_pop.png')
    

def category_freq():
    """
    This function does not take in any parameters. 
    It reads data from category_freq.json and creates a 
    pie chart to visualize the number of songs in each 
    sentiment category. The function does not return anything.
    """
    data = read_data_from_file('category_freq.json')
    labels = 'Negative', 'Postive', 'Neutral'
    colors = ['lightcoral', 'skyblue', 'lemonchiffon']
    explode = (0.1, 0, 0)
    sizes = []
    for item in data.items():
        sizes.append(int(item[1]))
    plt.figure()
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('Billboard Top 100 Hits Title Sentiments', pad=20)
    plt.savefig('category_freq.png')

def artist_freq():
    """
    This function does not take in any parameters. 
    It reads data from artist_freq.json and creates a 
    bar chart to visualize the artists with the most songs 
    in the Billboard Hot 100. The function does not return 
    anything.
    """
    data = read_data_from_file('artist_freq.json')
    artists = []
    frequency = []
    for item in data.items():
        artists.append(item[0])
        frequency.append(item[1])
    plt.figure()
    bars = plt.bar(artists, frequency)
    bars[0].set_color('lightcoral')
    bars[1].set_color('lemonchiffon')
    bars[2].set_color('skyblue')
    plt.title('Charting Dominance: Top Artists by Number of Billboard Top 100 Hits')
    plt.xlabel('Artist Name')
    plt.ylabel('Number of Songs')
    plt.savefig('artist_freq.png')


def popularity_and_sentiment():
    """
    This function does not take in any parameters. 
    It reads data from popularity_and_sentiment.json 
    and creates a scatterplot to visualize the correlation 
    between popularity and song title sentiment. The function 
    does not return anything.
    """
    data = read_data_from_file('popularity_and_sentiment.json')
    x = []
    y = []
    colors = colors = np.random.rand(len(data))
    for item in data:
        x.append(item['sentiment'])
        y.append(item['popularity'])
    plt.figure()
    plt.scatter(x, y, c=colors)
    plt.title('Popularity vs. Song Title Sentiment')
    plt.xlabel('Song Title Sentiment Score')
    plt.ylabel('Popularity Score')
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), color='black')
    plt.savefig('popularity_and_sentiment.png')


def main():
    avg_pop()
    category_freq()
    artist_freq()
    popularity_and_sentiment()

if __name__ == "__main__":
    main()
