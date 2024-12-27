import streamlit as st
# import speech_recognition as sr
# from googletrans import Translator

from menu import menu_with_redirect

menu_with_redirect()

st.title("💬 Chat with your Document")

# Initialize recognizer and translator
# recognizer = sr.Recognizer()
# translator = Translator()

def get_response(query: str):
    kb_details = st.session_state.kb_details
    kb_details.append({"kb_name": "Central Laws", "kb_path": "./storage/Central Laws"})
    kg = st.session_state.kg
    prompt = st.session_state.prompt
    kg.load_knowledge_graph(kb_details=kb_details, prompt=prompt)
    response = kg.query_knowledge_graph(query=query)
    return response

# Initialize session state for messages if not already done
if 'messages' not in st.session_state:
    st.session_state. messages = []

if st.session_state.kb_details == []:
    st.write("Knowledge Base is not selected")
else:
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Placeholder for the button to make it stay at the bottom
    # button_placeholder = st.empty()
    # with button_placeholder.container():
        # Add a speech-to-text button
        # if st.button("🎤 Speak"):
        #     with sr.Microphone() as source:
        #         with st.spinner("Listening..."):
        #             audio = recognizer.listen(source)

        #     try:
        #         # Recognize speech using Google Speech Recognition
        #         text = recognizer.recognize_google(audio, language='auto')  # 'auto' detects the language automatically
        #         # st.info(f"Recognized Text: {text}")

        #         # Add user message to chat history
        #         st.session_state.messages.append({"role": "user", "content": text})
        #         # Display user message in chat message container
        #         with st.chat_message("user"):
        #             st.markdown(text)

        #         # Display assistant response in chat message container
        #         with st.chat_message("assistant"):
        #             response = get_response(text)
        #             st.markdown(response)
        #         # Add assistant response to chat history
        #         st.session_state.messages.append({"role": "assistant", "content": response})

        #     except sr.UnknownValueError:
        #         st.error("Could not understand audio")
        #     except sr.RequestError as e:
        #         st.error(f"Could not understand audio: {e}")

    # Accept user input via text
    if prompt := st.chat_input("Enter your query"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = get_response(prompt)
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
