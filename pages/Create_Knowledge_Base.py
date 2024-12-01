import streamlit as st
import os
import json

from menu import menu_with_redirect

menu_with_redirect()

with open("data.json", "r") as jsonFile:
    data = json.load(jsonFile)

user = st.session_state.user

kbs = [db["kb_name"] for db in data["databases"][user]]

st.header("✏️ Upload Document")

kb_name = st.text_input("Enter your Knowledge Base name")

disabled = True

if kb_name:
    if kb_name in kbs:
        st.error("Knowledge Base already exists with this name. Give a unique name.")
    else:
        disabled = False

file = st.file_uploader("Upload your file", type=["pdf", "txt"])

if st.button("Create Knowledge Base", disabled=disabled):
    if file is not None:
        with st.status("Creating Knowledge Base") as status:
            file_name = file.name
            file_path = os.path.join("files", file_name)
            with open(file_path, "wb+") as f:
                f.write(file.getbuffer())
            kg = st.session_state.kg
            kg.create_knowledge_graph(file_name=file_name, kb_name=kb_name, user=user)
            os.remove(file_path)
            status.update(
                label="Knowledge Base Created",
                state="complete",
                expanded=False,
            )
    else:
        st.write("File is not uploaded")
