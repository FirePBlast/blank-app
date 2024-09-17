import streamlit as st

with st.form("my_form"):
    st.write("Inside the form")
    name = st.text_input('Your data')

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("Name:", name)
