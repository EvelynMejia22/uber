import pandas as pd
import numpy as np
import streamlit as st

st.title('Uber pickups in NYC :statue_of_liberty:')
st.subheader("Viajes de Uber en la ciudad de Nueva York con filtros por hora.")
st.write('By: Evelyn Mejía A01652115')


DATA_URL = 'https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz'


@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    return data

data_load_state = st.text('Loading data...')
data = load_data(1000)
data_load_state.text("Done! (using st.cache)")


df=pd.read_csv(DATA_URL)
df['Date/Time']=pd.to_datetime(df['Date/Time'])
df['hour']=df['Date/Time'].dt.strftime('%H')
df_hours=df['hour'].value_counts()
df_hours=pd.DataFrame(df_hours)
df_hours=df_hours.reset_index()
df_hours=df_hours.rename(columns={'index':'hour','hour':'count'})
df_hours=df_hours.sort_values(by='hour')

df['hour']=df['hour'].astype('int64')
df=df.rename(columns={"Lat": "lat", "Lon": "lon"})


# Some number in the range 0-23
optionals=st.sidebar.expander('Mapa',True)
hour_select=optionals.slider(
    'select the hour',
    min_value=int(df['hour'].min()),
    max_value=int(df['hour'].max()),
)

st.subheader('Map of all pickups at %s:00' % hour_select)
subset_hour=df[(df['hour'] == hour_select)]
map_data=subset_hour[['lat','lon']]

st.map(map_data)
