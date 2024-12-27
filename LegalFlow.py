import streamlit as st
from utils.kg import KG
from utils.prompts import public_prompt, professional_prompt
from menu import menu

import re
import json
import os

import pyotp
import qrcode

with open("data.json", "r") as jsonFile:
    data = json.load(jsonFile)

users = data["users"]
user_info = data["user_info"]


# Mock Authentication Function (Replace with your actual authentication logic)
def authenticate(username, password):
    # Example logic: Replace with actual validation logic
    # if username == "admin" and password == "password123":
    #     return True
    # return False

    return True


if "authenticated" not in st.session_state or not st.session_state["authenticated"]:

    tabs = st.tabs(["Login", "Register", "Enable Two-Factor Authentication (MFA)"])

    with tabs[0]:
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input(
            "Password", type="password", key="login_password"
        )

        if st.button("Login", key="login_button"):
            if password := user_info.get(login_username)["password"]:
                if password == login_password:
                    st.session_state.username = login_username
                    if user_info[login_username]["MFA"]:
                        st.switch_page("pages/MFA.py")
                    else:
                        st.session_state.user = login_username
                        st.session_state.user_type = user_info[login_username]["type"]
                        st.session_state["authenticated"] = True
                        st.rerun()  # Refresh the app after login to show content
                else:
                    st.error("The password that you have entered is incorrect")
            else:
                st.error("Invalid username")
    with tabs[1]:
        username_check = False
        password_check = False
        confirm_password_check = False

        reg_username = st.text_input("Username", key="reg_username")
        if reg_username:
            if reg_username in users:
                st.error("Username already exists")
            else:
                username_check = True

        reg_password = st.text_input(
            "Password",
            type="password",
            key="reg_password",
            help="Password should atleast contain 8 characters with atleast 1 uppercase, 1 lowercase and 1 special character",
        )
        if reg_password:
            if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,}$", reg_password):
                st.error("Password is weak")
                st.error(
                    "Password should contain atleast 8 characters with atleast 1 uppercase, 1 lowercase and 1 special character"
                )
            else:
                password_check = True

        reg_conf_password = st.text_input(
            "Confirm Password", type="password", key="reg_conf_password"
        )
        if reg_conf_password:
            if reg_password != reg_conf_password:
                st.error("Password and Confirm Password doesn't match")
            else:
                confirm_password_check = True

        reg_user_type = st.selectbox(
            label="Select user type", options=["Select an option", "Legal Professional", "General Public"]
        )

        if st.button(
            "Register",
            disabled=(not username_check & password_check & confirm_password_check & (reg_user_type != "Select an option")),
            key="register_button",
        ):
            data["users"].append(reg_username)
            data["user_info"].update(
                {reg_username: {"password": reg_password, "MFA": False, "type" : reg_user_type}}
            )
            data["databases"].update({reg_username: []})

            with open("data.json", "w") as jsonFile:
                json.dump(data, jsonFile)

            st.session_state.user = reg_username
            st.session_state.user_type = reg_user_type
            st.session_state["authenticated"] = True
            st.rerun()

    with tabs[2]:
        fa_username = st.text_input("Username", key="fa_username")

        disabled = True

        if fa_username:
            if info := user_info.get(fa_username):
                if info["MFA"]:
                    st.error("MFA has already been setup for this account")
                else:
                    disabled = False
            else:
                st.error("Invalid username")

        fa_password = st.text_input("Password", type="password", key="fa_password")

        if st.button("Enable MFA", key="MFA_create_button", disabled=disabled):
            if info["password"] == fa_password:
                mfa_uri = pyotp.totp.TOTP(fa_username).provisioning_uri(
                    name=fa_username, issuer_name="HR_RAG"
                )
                qrcode.make(mfa_uri).save("./qr.png")
                data["user_info"].get(fa_username).update({"MFA": True})
                with open("data.json", "w") as jsonFile:
                    json.dump(data, jsonFile)
                st.switch_page("pages/QR.py")
            else:
                st.error("The password that you have entered is incorrect")

else:
    with st.spinner("Creating LLM and Embedding Model instances") as spin:
        if "kg" not in st.session_state:
            st.session_state.kg = knowledge_graph = KG()

        if "messages" not in st.session_state:
            st.session_state.messages = []

        if "judgement_messages" not in st.session_state:
            st.session_state.judgement_messages = []

        if 'central_messages' not in st.session_state:
            st.session_state.central_messages = []

        if "kb_details" not in st.session_state:
            st.session_state.kb_details = []

        if "prompt" not in st.session_state:
            if st.session_state.user_type == "General Public":
                st.session_state.prompt = public_prompt
            elif st.session_state.user_type == "Legal Professional":
                st.session_state.prompt = professional_prompt
    markdown_content = """
# Welcome to LegalFlow 🏛️  

**LegalFlow** is your go-to platform for understanding and navigating complex legal documents. Whether you're a legal professional or a general user, our intelligent chatbot is here to provide accurate, insightful, and easy-to-understand answers to your legal queries.  

We aim to bridge the gap between legal complexity and accessibility. By leveraging the latest advancements in AI, our platform delivers unparalleled legal insights to empower users with accurate and actionable information.  

**Simplifying Laws, Empowering Decisions, LegalFlow!**  
    """
    st.markdown(markdown_content)

menu()
