import streamlit as st
import pre_processor, helper

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