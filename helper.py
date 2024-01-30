import pandas as pd
from collections import Counter
# from wordcloud import WordCloud
from urlextract import URLExtract
import emoji 
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


def most_busy_users(df):
    # most busy users
    x = df['user'].value_counts().head()
    # individual persantage of messages
    per_df = round((df['user'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns={'count': 'percentage', 'user': 'name'})
    return x, per_df

# def create_wordcloud(selected_user, df):
#     if selected_user != 'Overall':
#         df = df[df.user == selected_user]

#     wc = WordCloud(width=760, height=480, min_font_size=10, background_color='white')
#     # remove media ommited msg
#     df = df[df.message != '<Media omitted>\n']
#     #  remove group notification
#     df = df[df.user != 'group_notification']
#     wc.generate(' '.join(df['message']))
#     wc_df = wc.generate(df['message'].str.cat(sep=' '))
#     return wc_df

def most_common_words(selected_user, df):
    f = open('stop_words.txt', 'r', encoding='utf-8')
    stop_words = f.read().split('\n')
    if selected_user != 'Overall':
        df = df[df.user == selected_user]

    # remove media ommited msg
    df = df[df.message != '<Media omitted>\n']
    #  remove group notification
    df = df[df.user != 'group_notification']
    # remove stop words
    words = []
    for msg in df['message']:
        for word in msg.split():
            if word.lower() not in stop_words:
                words.append(word.lower())

    top_20 = Counter(words).most_common(20)
    top_20 = pd.DataFrame(top_20).rename(columns={0: 'word', 1: 'count'})
    return top_20

def most_common_emojis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df.user == selected_user]

    emojis = []
    for msg in df['message']:
        for char in msg:
            if emoji.is_emoji(char):
                emojis.append(char)

    top_20 = Counter(emojis).most_common(20)
    top_20 = pd.DataFrame(top_20).rename(columns={0: 'emoji', 1: 'count'})
    return top_20


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df.user == selected_user]

    timeline = df.groupby(['year', 'month']).count()['message'].reset_index()
    timeline['period'] = timeline['month'].astype(str) + '-' + timeline['year'].astype(str)
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df.user == selected_user]

    daily_timeline = df.groupby(df['date'].dt.date).count()['message'].reset_index()
    return daily_timeline

def weekly_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df.user == selected_user]
    return df['day_name'].value_counts()

def monthly_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df.user == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df.user == selected_user]
    
    table = pd.pivot_table(df, values='message', index=['day_name'], columns=['hour'], aggfunc='count', fill_value=0)
    return table