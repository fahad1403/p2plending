import streamlit as st
from alraedah_investor import investor_main
from userapp import business_main

st.markdown('<h1 class="title">Welcome to Alraedah</h1>',unsafe_allow_html=True)
login_type = st.selectbox("Please Select", ("I'm an investor", "I'm a business"))
if login_type=="I'm an investor":
    if st.button("Login"):
        investor_main()
elif login_type=="I'm a business":
    if st.button("Login"):
        business_main()