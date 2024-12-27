import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    # st.sidebar.page_link("auth.py", label="Switch accounts")
    st.sidebar.page_link("LegalFlow.py", label="Home", icon="🏠")
    st.sidebar.page_link(
        "pages/Chat_with_Central_Laws.py",
        label="The Constitution Chatbot",
        icon="⚖️"
    )
    if st.session_state.user_type == "Legal Professional":
        st.sidebar.page_link(
            "pages/Refer_Judgements.py",
            label="Refer Judgements",
            icon="👨‍⚖️"
        )
    st.sidebar.page_link(
        "pages/Create_Knowledge_Base.py", label="Upload Document", icon="✏️"
    )
    st.sidebar.page_link(
        "pages/Choose_Knowledge_Base.py", label="Choose Document", icon="✅"
    )
    st.sidebar.page_link(
        "pages/Chat_With_Knowledge_Base.py",
        label="Chat with your Document",
        icon="💬",
    )


    if st.sidebar.button("Logout"):
        st.session_state.messages = []
        st.session_state.judgement_messages = []
        st.session_state.central_messages = []
        st.session_state.kb_details = []
        st.session_state["authenticated"] = False
        st.switch_page("LegalFlow.py")


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("LegalFlow.py", label="Log in")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        # unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.switch_page("LegalFlow.py")
    menu()
