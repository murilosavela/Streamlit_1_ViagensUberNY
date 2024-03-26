import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title='Viagens Uber', page_icon='https://p2.trrsf.com/image/fget/cf/1200/900/middle/images.terra.com/2022/07/22/517909072-i500561.jpeg', layout='wide')

st.title('Embarque e desembarque de Uber em Nova York')


DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")


if st.checkbox('Ver base de dados'):
    st.subheader('Dados')
    st.write(data)

st.subheader('Número de viagens por hora')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values)


hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Mapa de todas as viagens às {hour_to_filter}:00')
st.map(filtered_data)