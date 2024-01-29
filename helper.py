import pandas as pd
from urlextract import URLExtract
extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df.user == selected_user]

    # 1. total msgs
    total_msgs = df.shape[0]
    # 2. total words
    total_words = df.message.str.split().apply(len).sum()
    # 3. total media files
    total_media = df[df.message == ('<Media omitted>\n')].shape[0]
    # 4. total links
    links = []
    for idx, row in df.iterrows():
        links.extend(extract.find_urls(row['message']))
    total_links = len(links)

    return total_msgs, total_words, total_media, total_links