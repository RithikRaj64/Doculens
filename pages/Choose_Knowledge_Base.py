import streamlit as st
import json

from menu import menu_with_redirect

menu_with_redirect()

st.header("✅ Choose Document")

with open("data.json", "r") as jsonFile:
    data = json.load(jsonFile)

user = st.session_state.user

user_kbs = data["databases"].get(user)

kbs = [db["kb_name"] for db in user_kbs]

# kbs.remove("Central Laws")

kb_names = st.multiselect(
    label="Knowledge Base List", options=kbs, placeholder="Select your KB(s)"
)

kb = [db for db in user_kbs if db["kb_name"] in kb_names]

if len(kbs) == 0:
    st.write("There are no Knowledge Bases")
else:
    if st.button("Choose"):
        st.session_state.kb_details = kb
        st.write(
            "Knowledge Base(s) Selected. Now you can chat with it in the Chat With Knowledge Base page"
        )
