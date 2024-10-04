import streamlit as st
import pandas as pd
import requests
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode


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
        submit_sql_button = st.form_submit_button("Afficher les données")
        
        selected_table = {
            "table_name" : tb_name
        }
            
        if submit_sql_button:
            if tb_name:
                response = requests.get(request_url, params=selected_table)
                if response.status_code == 200:
                    data = response.json()
                    columns = data[0]
                    rows = data[1]
            
                    df = pd.DataFrame(rows, columns=columns)
                    st.dataframe(df)
                    df['selected'] = True 

                    gb = GridOptionsBuilder.from_dataframe(df)
                    gb.configure_column("selected", headerCheckboxSelection = True, checkboxSelection = True)
                    gb.configure_grid_options(fit_columns_on_grid_load=True)
                    gridOptions = gb.build()
            
                    grid_response = AgGrid(
                        df,
                        gridOptions=gridOptions,
                        update_mode=GridUpdateMode.MODEL_CHANGED,
                        allow_unsafe_jscode=True,
                    )
            
                    selected_rows = grid_response['selected_rows']
                    selected_ids = [row['id_conversation'] for row in selected_rows]

                    if st.form_submit_button("Fine-tune Model"):
                        request_url = st.session_state['url'] + "/fine_tune"
                        if selected_ids:
                            # Make API call to fine-tune the model with selected IDs
                            response_tune = requests.post(request_url, json={"conversation_ids": selected_ids})
                            
                            if response_tune.status_code == 200:
                                st.success("Fine-tuning job submitted successfully!")
                            else:
                                st.error("Error submitting fine-tuning job.")
                    
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


        

