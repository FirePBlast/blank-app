import streamlit as st

with st.form("my_form"):
    st.title('Formulaire de prédiction')

    longitude = st.number_input('Longitude')
    latitude = st.number_input('Latitude')
    housing_median_age = st.number_input('Housing Median Age')
    total_rooms = st.number_input('Total Rooms')
    total_bedrooms = st.number_input('Total Bedrooms')
    population = st.number_input('Population')
    households = st.number_input('Households')
    median_income = st.number_input('Median Income')

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

    response = requests.post('https://5acd-34-70-132-187.ngrok-free.app/predict', json=data)
    
    if response.status_code == 200:
        prediction = response.json()['Prédiction']
        st.success(f'La prédiction est : {prediction}')
    else:
        st.error('Erreur lors de la prédiction')

