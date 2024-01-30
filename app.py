import streamlit as st
import pre_processor, helper
import plotly.express as px

# create title with  
st.sidebar.image("https://www.freepnglogos.com/uploads/whatsapp-logo-light-green-png-0.png", width=150)
st.sidebar.title("WhatsApp Chat Analysis 📊")

# Upload chat file
uploaded_file = st.sidebar.file_uploader(
    label="Upload your WhatsApp Chat",
    type=['txt'],
    accept_multiple_files=False
)
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = pre_processor.preprocess(data)
    st.dataframe(df)

    # fetch unque user
    user_list = df.user.unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_msg, num_words, total_media, total_links = helper.fetch_stats(selected_user, df)
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.header("Total Messages")
            st.title(num_msg)

        with c2:
            st.header("Total Words")
            st.title(num_words)

        with c3:
            st.header("Media Shared")
            st.title(total_media)

        with c4:
            st.header("Total Links")
            st.title(total_links)

        # Top Users Activity
        if selected_user == 'Overall':
            st.title("Users Activity")
            c1, c2 = st.columns(2)

            with c1:
                st.header("Most Busy Users")
                x, per_df = helper.most_busy_users(df)
                fig = px.bar(x, x=x.values, y=x.index, orientation='h', )
                st.plotly_chart(fig)

            with c2:
                st.header("Individual Contribution")
                st.dataframe(per_df)

        # Word Cloud
        st.title("Word Cloud")
        word_cloud = helper.create_wordcloud(selected_user, df)
        st.image(word_cloud.to_image())

        # Most Common Words
        st.title("Most Common Words")
        most_common_words = helper.most_common_words(selected_user, df)
        fig = px.bar(most_common_words, x='word', y='count')
        st.plotly_chart(fig)

        # Most Common Emojis
        st.title("Most Common Emojis")
        emoji_df = helper.most_common_emojis(selected_user, df)
        # create pie chart 
        fig = px.pie(emoji_df, values='count', names='emoji')
        st.plotly_chart(fig)


