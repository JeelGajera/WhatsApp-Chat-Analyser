import streamlit as st
import pre_processor, helper
import plotly.express as px

# set page configuration
st.set_page_config(
    page_title="WhatsApp Chat Analysis",
    page_icon="https://img.icons8.com/3d-fluency/94/combo-chart.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': "https://github.com/JeelGajera/WhatsApp-Chat-Analyser",
        'Report a bug': "https://github.com/JeelGajera/WhatsApp-Chat-Analyser/issues",
        'About': "This Python project is designed to analyze WhatsApp chat data, providing valuable insights and visualizations from the conversation history. The script processes exported chat text files and extracts relevant information for in-depth analysis."
    }
)

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

    # fetch unque user
    user_list = df.user.unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        st.title("📊 Top Statistics")
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

        # Timeline Analysis
        st.title(f"🗓️ Timeline Analysis Statistics of {selected_user}")

        # Monthly Timeline
        st.header("Monthly Timeline")
        timeline_df = helper.monthly_timeline(selected_user, df)
        fig = px.line(timeline_df, x='period', y='message')
        st.plotly_chart(fig)

        # Daily Timeline
        st.header("Daily Timeline")
        timeline_df = helper.daily_timeline(selected_user, df)
        fig = px.line(timeline_df, x='date', y='message')
        st.plotly_chart(fig)

        # Activity Map
        c1, c2 = st.columns(2)
        with c1:
            st.header("Monthly Activity Map")
            monthly_activity_df = helper.monthly_activity_map(selected_user, df)
            fig = px.bar(monthly_activity_df, x=monthly_activity_df.index, y=monthly_activity_df.values)
            fig.update_xaxes(title_text='Months')
            fig.update_yaxes(title_text='Counts')
            st.plotly_chart(fig)

        with c2:
            st.header("Weekly Activity Map")
            weekly_activity_df = helper.weekly_activity_map(selected_user, df)
            fig = px.pie(weekly_activity_df, values=weekly_activity_df.values, names=weekly_activity_df.index)
            st.plotly_chart(fig)

        # Top Users Activity
        if selected_user == 'Overall':
            st.title("🧑‍💻 Users Activity")
            c1, c2 = st.columns(2)

            with c1:
                x, per_df = helper.most_busy_users(df)
                st.header("Individual Contribution")
                st.dataframe(per_df)
            with c2:
                st.header("Most Busy Users")
                fig = px.bar(x, x=x.values, y=x.index, orientation='h', )
                st.plotly_chart(fig)

        # Word Cloud
        st.title("🌨️ Word Cloud")
        word_cloud = helper.create_wordcloud(selected_user, df)
        st.image(word_cloud.to_image())

        # Most Common Words
        st.title("🤐 Most Common Words")
        most_common_words = helper.most_common_words(selected_user, df)
        fig = px.bar(most_common_words, x='word', y='count')
        st.plotly_chart(fig)

        # Most Common Emojis
        st.title("😎 Most Common Emojis")
        emoji_df = helper.most_common_emojis(selected_user, df)
        fig = px.pie(emoji_df, values='count', names='emoji')
        st.plotly_chart(fig)


    
        st.title('🛠️ Pre-Processed Chat Data')
        st.dataframe(df)
    else:
        st.title("WhatsApp Chat Analysis 📊")
        st.info("Click on Show Analysis button to start analysis")

else:
    # show info if data is not uploaded
    st.title("WhatsApp Chat Analysis 📊")
    st.info("Upload your WhatsApp Chat data")

# add footer to sidebar
st.sidebar.markdown(
    """
    <div> <strong>< /></strong> with ❤️ by <a href="https://github.com/JeelGajera" target="_blank" style="text-decoration: none; color: white; text-decoration: underline;">Jeel Gajera</a> </div>
    """,
    unsafe_allow_html=True
)