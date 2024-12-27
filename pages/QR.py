import streamlit as st

import os

st.image(
    "./qr.png",
    caption="Scan and add your MFA code in an Authentication app before proceeding",
)
if st.button("Scanned MFA code"):
    os.remove("./qr.png")
    st.switch_page("HR_RAG.py")
