import streamlit as st
import pandas as pd
import requests

st.title("Bot")

if 'url' not in st.session_state:
    st.session_state['url'] = ''

# Fonctions pour chaque page
def page1():

    request_url = st.session_state['url'] + "/question"
    
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
        response = requests.get(request_url, params=data)
        
        if response.status_code == 200:
            response_content = response.json()  # Extrayez le contenu JSON
        else:
            response_content = f"Erreur : {response.status_code}"
             
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response_content )
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_content })

def page2():
    st.title("Lecture de Table")
    table_names = ["model", "metrics", "conversation"]
    request_url = st.session_state['url'] + "/read_table"
    
    with st.form("table_form"):
        tb_name = st.selectbox("Sélectionnez une table", table_names)
        selected_table ={
            "table_name" = tb_name
        }
        submit_sql_button = st.form_submit_button("Afficher les données")
    
        if submit_sql_button:
            if selected_table:
                response = requests.get(request_url, params=selected_table)
                if response.status_code == 200:
                    st.write(f"Données de la table '{selected_table}':")
                    data = response.json()
                    columns = data[0]
                    rows = data[1]
            
                    df = pd.DataFrame(rows, columns=columns)
                    st.dataframe(df)
                else:
                    st.write(f"Erreur : {response.status_code}")

    
def page3():
    st.title("Page 3")

pages = {
    "Chat Bot": page1,  
    "Lecture de Table": page2,
    "Monitoring": page3,
}

with st.sidebar:
    st.title("Sidebar")
    user_input = st.text_input("Entrez l'url")
    submit_button = st.button("Valider")

    if submit_button:
        st.session_state['url'] = user_input
        
    selected_page = st.radio("Sélectionnez une page", list(pages.keys()))
    
if selected_page:
    pages[selected_page]()


        

