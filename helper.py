import pandas as pd

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
    total_links = df[df.message.str.contains('http')].shape[0]

    return total_msgs, total_words, total_media, total_links