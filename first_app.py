import streamlit as st

st.title('My first Streamlit app')

st.write('Welcome to my Streamlit app!')

st.button("Reset", type="primary")
if st.button("Say Hello"):
  st.write("Why hello there")
else:
  st.write("Goodbye")