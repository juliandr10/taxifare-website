import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.title('TaxiFareModel Frontend')

st.markdown('''
TaxiFareModel Frontend by Juli, thank you for using our services.
''')

st.header('Select the parameters of the ride')

date_time = st.text_input('Enter the date and time of the ride (YYYY-MM-DD HH:MM:SS)', value=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
pickup_longitude = st.number_input('Enter the pickup longitude', value=-73.985428)
pickup_latitude = st.number_input('Enter the pickup latitude', value=40.748817)
dropoff_longitude = st.number_input('Enter the dropoff longitude', value=-73.985428)
dropoff_latitude = st.number_input('Enter the dropoff latitude', value=40.748817)
passenger_count = st.number_input('Enter the passenger count', min_value=1, max_value=8, value=1)

if pickup_latitude and pickup_longitude and dropoff_latitude and dropoff_longitude:
    map_data = pd.DataFrame({
        'lat': [pickup_latitude, dropoff_latitude],
        'lon': [pickup_longitude, dropoff_longitude]
    })

    st.map(map_data)

if st.button('Get Fare Prediction'):

    params = {
        'pickup_datetime': date_time,
        'pickup_longitude': pickup_longitude,
        'pickup_latitude': pickup_latitude,
        'dropoff_longitude': dropoff_longitude,
        'dropoff_latitude': dropoff_latitude,
        'passenger_count': passenger_count
    }

    url = 'http://localhost:8000/predict'
    response = requests.get(url, params=params)

    if response.status_code == 200:
        prediction = response.json().get('fare', 'Error: No fare returned')
        st.success(f'The predicted fare is: ${prediction:.2f}')
    else:
        st.error('Error in API call. Please check your input or try again later.')
