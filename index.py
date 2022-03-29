import streamlit as st
import py_scripts.helper.read_chat_DM
st.sidebar.title("WhatsUp")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    data = py_scripts.helper.read_chat_DM.getMessages(data)
    st.dataframe(data)
    print(data.shape[0])