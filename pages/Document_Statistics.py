import streamlit as st
import json

from menu import menu_with_redirect

menu_with_redirect()

st.header("✅ Document Statistics")

if kb_details := st.session_state.kb_details:
    for kb in kb_details:
        if "metadata" in kb:
            st.write(kb["metadata"])