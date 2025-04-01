import streamlit as st

with st.sidebar:
    if not st.experimental_user.is_logged_in:
        st.button("Log in", on_click=st.login,args=("google",))
        st.stop()

    st.write("Log out",on_click=st.logout,args=("google",))