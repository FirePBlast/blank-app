import streamlit as st
import requests

with st.sidebar.form("my_form_sidebar"):
    text_input = st.text_input('Nom Modèle')
    submitted = st.form_submit_button("Changer le modèle")
    if submitted:
        response = requests.post('https://fb9f-34-70-132-187.ngrok-free.app/new_model', params={name:model_name})
        if response.status_code == 200:
            st.success('Le nouveau modèle a été chargé')
        else:
             st.error('Erreur lors du chargement du modèle')


with st.form("my_form"):
    st.title('Formulaire de prédiction')

    longitude = st.slider('Longitude', min_value=-180.0, max_value=180.0, value=0.0)
    latitude = st.slider('Latitude', min_value=-90.0, max_value=90.0, value=0.0)
    housing_median_age = st.slider('Housing Median Age', min_value=0, max_value=100, value=50)
    total_rooms = st.slider('Total Rooms', min_value=0, max_value=10000, value=5000)
    total_bedrooms = st.slider('Total Bedrooms', min_value=0, max_value=5000, value=2500)
    population = st.slider('Population', min_value=0, max_value=10000, value=5000)
    households = st.slider('Households', min_value=0, max_value=5000, value=2500)
    median_income = st.slider('Median Income', min_value=0, max_value=5000, value=500)

    submitted = st.form_submit_button("Prédire")
    if submitted:
        
        data = {
            'longitude': longitude,
            'latitude': latitude,
            'housing_median_age': housing_median_age,
            'total_rooms': total_rooms,
            'total_bedrooms': total_bedrooms,
            'population': population,
            'households': households,
            'median_income': median_income
        }

        response = requests.post('https://fb9f-34-70-132-187.ngrok-free.app/predict', json=data)
    
        if response.status_code == 200:
            prediction = response.json()['Prédiction']
            st.success(f'La prédiction est : {prediction}')
        else:
            st.error('Erreur lors de la prédiction')

