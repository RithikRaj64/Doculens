import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    # st.sidebar.page_link("auth.py", label="Switch accounts")
    st.sidebar.page_link("Doculens.py", label="Home", icon="🏠")

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
    st.sidebar.page_link(
        "pages/Document_Statistics.py",
        label="Get Document Statistics",
        icon="💬",
    )

    if "kb_details" not in st.session_state:
        st.session_state.kb_details = []

    if kb_details := st.session_state.kb_details:
        st.sidebar.header("Chosen Knowledge Bases")

        # Create a dictionary to store checkboxes for each KB
        selected_kbs = {}

        # Render a checkbox for each KB
        for kb in kb_details:
            selected_kbs[kb["kb_name"]] = st.sidebar.checkbox(kb["kb_name"], key=kb["kb_name"])

        # Button to delete selected KBs
        if st.sidebar.button("Delete Selected KBs"):
            # Filter out the KBs that were selected
            st.session_state.kb_details = [
                kb for kb in kb_details if not selected_kbs[kb["kb_name"]]
            ]
            st.sidebar.success("Selected Knowledge Bases have been deleted.")
            st.rerun()

    if st.sidebar.button("Logout"):
        st.session_state.messages = []
        st.session_state.judgement_messages = []
        st.session_state.central_messages = []
        st.session_state.kb_details = []
        st.session_state["authenticated"] = False
        st.switch_page("Doculens.py")
    



def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("Doculens.py", label="Log in")


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
        st.switch_page("Doculens.py")
    menu()
