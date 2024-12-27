import streamlit as st

import pyotp

st.header("Multi-Factor Authentication")

username = st.session_state.username

mfa_code = st.text_input("Enter MFA code")

if st.button("Verify MFA code"):
    totp = pyotp.TOTP(username)
    if totp.verify(mfa_code):
        st.session_state.user = username
        st.session_state["authenticated"] = True
        st.switch_page("HR_RAG.py")
    else:
        st.error("Incorrect MFA code")
