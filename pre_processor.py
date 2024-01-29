import re
import pandas as pd


# Create Data Frame of the WhatsApp Chat Text
def preprocess(data) -> pd.DataFrame:
    # Regex for split message and date
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # create data frame 
    df = pd.DataFrame({'date': dates, 'user_message': messages})
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %H:%M - ')

    # saprate user name and msg
    users = []
    messages = []
    for msg in df['user_message']:
        msg_str = re.split('([\w\W]+?):\s', msg)
        if msg_str[1:]:
            users.append(msg_str[1])
            messages.append(msg_str[2])
        else:
            users.append('group_notification')
            messages.append(msg_str[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Create date time columns
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df