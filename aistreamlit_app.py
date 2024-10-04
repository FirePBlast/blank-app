import streamlit as st
import requests

st.title("Bot")

if 'url' not in st.session_state:
    st.session_state['url'] = ''

pages = {
    "Page 1": "page1",
    "Page 2": "page2",
    "Page 3": "page3",
}

def page1():
    st.title("Page 1")
    # ... code pour la page 1

def page2():
      st.title("Formulaire de la page 2")
      email = st.text_input("Email")
      country = st.selectbox("Pays", ["France", "USA", "Canada"])

def page3():
    st.title("Page 3")
    # ... code pour la page 3

with st.sidebar:
    st.title("Sidebar")
    user_input = st.text_input("Entrez l'url")
    submit_button = st.button("Valider")

    if submit_button:
        st.session_state['url'] = user_input
        
    selected_page = st.radio("Sélectionnez une page", list(pages.keys()))
    
if selected_page:
    pages[selected_page]()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # url = 'https://42b8-34-168-18-253.ngrok-free.app/question'
    
    data={
        "prompt" : prompt
    }
    response = requests.get(st.session_state['url'], params=data)
    
    if response.status_code == 200:
        response_content = response.json()  # Extrayez le contenu JSON
    else:
        response_content = f"Erreur : {response.status_code}"
         
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response_content )
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_content })

        

