
import requests
from bs4 import BeautifulSoup
import lyricsgenius
import time
import pandas as pd
import re
import nltk
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from langdetect import detect
from tabulate import tabulate 
import json
from scipy.stats import kendalltau
import shutil
import os
nltk.download('punkt') 

def get_billboard_hot_100():
    """Scrapes the current Billboard Hot 100 song titles."""
    url = "https://www.billboard.com/charts/hot-100/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    song_data = []
    
    for item in soup.select("li.o-chart-results-list__item h3"):
        song_title = item.get_text(strip=True)
        if song_title:
            song_data.append(song_title)

    return song_data[:100]

def get_melon_chart():
    """Scrapes the current Melon Chart Top 100 song titles."""
    url = "https://www.melon.com/chart/index.htm"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    song_data = []
    
    for item in soup.select("div.ellipsis.rank01 a"):
        song_title = item.get_text(strip=True)
        if song_title:
            song_data.append(song_title)

    return song_data[:100]

# Fetch top songs
billboard_songs = get_billboard_hot_100()
melon_songs = get_melon_chart()

print(f"Fetched {len(billboard_songs)} Billboard songs.")
print(f"Fetched {len(melon_songs)} Melon songs.")

# Add Genius API credentials
ACCESS_TOKEN = "Mfo9jwo2FTtUyLzzE7x2Ay4ELhGzPsrM1_sll9CN1-rQ_wV1l-6hQGWNk5IkonZx"
genius = lyricsgenius.Genius(ACCESS_TOKEN)

def get_lyrics_from_genius(song_list, target_language=None, target_count=10):
    collected_lyrics = []
    attempts = 0
    while len(collected_lyrics) < target_count and attempts < len(song_list):
        title = song_list[attempts]
        try:
            print(f"Searching lyrics for: {title}...")
            song = genius.search_song(title)
            if song and song.lyrics:
                lyrics_clean = re.sub(r"\[.*?\]", "", song.lyrics.replace("\n", " "))
                lyrics_clean = re.sub(r"[^\uAC00-\uD7A3a-zA-Z0-9\s]", "", lyrics_clean)  # Keep Hangul, English, and numbers
                if target_language and detect(lyrics_clean) != target_language:
                    print(f" - Skipped: Language mismatch")
                else:
                    collected_lyrics.append(lyrics_clean)
                    print(f" + Lyrics fetched for: {title}")
        except Exception as e:
            print(f" ! Error fetching {title}: {e}")
        attempts += 1
        time.sleep(1)
    return collected_lyrics

english_lyrics_list = get_lyrics_from_genius(billboard_songs, target_language="en", target_count=25)
korean_lyrics_list = get_lyrics_from_genius(melon_songs, target_language="ko", target_count=25)

#Analyze Word Frequency and Length
def analyze_zipf_law(lyrics_list):
    full_text = " ".join(lyrics_list).lower()
    tokens = [t for t in nltk.word_tokenize(full_text) if t.isalpha() and len(t) >= 2]
    word_counts = Counter(tokens)
    df = pd.DataFrame({"word": list(word_counts.keys()), "frequency": list(word_counts.values()), "length": [len(w) for w in word_counts.keys()]})
    df = df[df['word'].str.match(r'^[a-zA-Z\uAC00-\uD7A3]+$')]  # Remove unwanted mixed character sequences
    df = df[~df['word'].str.contains("contributor|translations|romanization|lyrics|vitbahasa|indonesianederlands|phasa|thaipolskieskydie", case=False)]  # Remove unwanted words that kept showing up
    df = df[df['word'].str.match(r'^[a-zA-Z]+$|^[\uAC00-\uD7A3]+$')] #Remove English words mixed in Korean
    print(tabulate(df.head(25), headers="keys", tablefmt="grid"))  # Print formatted table
    return df

english_word_data = analyze_zipf_law(english_lyrics_list)
korean_word_data = analyze_zipf_law(korean_lyrics_list)

#Plot Zip´s Law
def plot_zipf(word_data, language_label="English"):
    plt.figure(figsize=(7, 5))
    sns.scatterplot(data=word_data, x="frequency", y="length", alpha=0.3)
    plt.xscale("log")
    plt.xlabel("Word Frequency (log scale)")
    plt.ylabel("Word Length")
    plt.title(f"Zipf’s Law of Abbreviation ({language_label})")
    plt.show()

plot_zipf(english_word_data, "English (Billboard)")
plot_zipf(korean_word_data, "Korean (Melon)")

#Compute Kendall's Correlation
def kendall_corr(word_data):
    return kendalltau(word_data["frequency"], word_data["length"])

print(f"English Kendall correlation: {kendall_corr(english_word_data)[0]:.3f}")
print(f"Korean Kendall correlation: {kendall_corr(korean_word_data)[0]:.3f}")


#Save Files 
def save_lyrics(lyrics_list, filename):
    """Saves lyrics to a TXT file."""
    if lyrics_list:
        with open(filename, "w", encoding="utf-8") as file:
            for i, lyrics in enumerate(lyrics_list):
                file.write(f"--- SONG {i+1} ---\n")
                file.write(lyrics + "\n\n")
        print(f"✅ Lyrics saved to {filename}")
    else:
        print(f"❌ ERROR: Lyrics list is empty, no file saved: {filename}")

# Save English and Korean lyrics
save_lyrics(english_lyrics_list, "English_lyrics.txt")
save_lyrics(korean_lyrics_list, "Korean_lyrics.txt")

def save_word_data(df, filename):
    """Saves word frequency data to a CSV file."""
    if not df.empty:
        df.to_csv(filename, index=False, encoding="utf-8")
        print(f"✅ Word data saved to {filename}")
    else:
        print(f"❌ ERROR: Word data is empty, no file saved: {filename}")

# Save word frequency data
save_word_data(english_word_data, "English_word_data.csv")
save_word_data(korean_word_data, "Korean_word_data.csv")

download_path = os.path.join(os.path.expanduser("~"), "Downloads")

def move_file_for_download(filename):
    """Moves file to a local Downloads folder (Windows/Mac/Linux safe)."""
    destination = os.path.join(download_path, filename)
    if os.path.exists(filename):
        shutil.move(filename, destination)
        print(f"✅ {filename} has been moved to {destination}. You can find it in your Downloads folder.")
    else:
        print(f"❌ ERROR: {filename} not found!")

# Move files to a local folder for easy access
move_file_for_download("English_lyrics.txt")
move_file_for_download("Korean_lyrics.txt")
move_file_for_download("English_word_data.csv")
move_file_for_download("Korean_word_data.csv")