import streamlit as st
import datetime
import requests
import pandas as pd
import pydeck as pdk


# Set Streamlit page configuration
st.set_page_config(page_title="NYC Taxi Fare Website", page_icon="🚖", layout="wide")


# '''
# # TaxiFare Website 🚖
# '''

#st.markdown('''
# Remember that there are several ways to output content into your web page...

# Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
# ''')

st.title("🚖 NYC Taxi Fare Prediction")
'''
## Ride details
'''
# Select Date and Time separately, then combine them
date = st.date_input("Select Date", datetime.date.today())
time = st.time_input("Select Time", datetime.datetime.now().time())

# Merge into a single datetime object
datetime_input = datetime.datetime.combine(date, time)

pickup_longitude = st.number_input("Pickup Longitude")
pickup_latitude = st.number_input("Pickup Latitude")
dropoff_longitude = st.number_input("Dropoff Longitude")
dropoff_latitude = st.number_input("Dropoff Latitude")
passenger_count = st.number_input("Passenger Count", min_value=1, step=1)

st.write("### Selected Ride Details:")
st.write(f"📅 Date & Time: {datetime_input}")
st.write(f"📍 Pickup Coordinates: ({pickup_latitude}, {pickup_longitude})")
st.write(f"📍 Dropoff Coordinates: ({dropoff_latitude}, {dropoff_longitude})")
st.write(f"👥 Passenger Count: {passenger_count}")

# 1. Let's ask for:
# - date and time
# - pickup longitude
# - pickup latitude
# - dropoff longitude
# - dropoff latitude
# - passenger count
# '''

# '''
# ## Once we have these, let's call our API in order to retrieve a prediction

# See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

# 🤔 How could we call our API ? Of course... The `requests` package 💡
# '''

url = 'https://taxifare-921811459342.europe-west1.run.app/predict'
params = {
    'pickup_datetime': datetime_input,
    'pickup_longitude': pickup_longitude,
    'pickup_latitude': pickup_latitude,
    'dropoff_longitude': dropoff_longitude,
    'dropoff_latitude': dropoff_latitude,
    'passenger_count': passenger_count
}
response = requests.get(url, params=params)
prediction = response.json()

st.write("### Predicted Fare:")
st.write(f"💰 {round(prediction['fare'],2)}")


st.subheader("📌 Route:")

# Data for the pickup and dropoff points
map_data = pd.DataFrame(
    [
        {"lat": pickup_latitude, "lon": pickup_longitude, "type": "Pickup"},
        {"lat": dropoff_latitude, "lon": dropoff_longitude, "type": "Dropoff"},
    ]
)

map_data["colour"] = map_data["type"].map({"Pickup": [0, 255, 0], "Dropoff": [255, 0, 0]})  # Green for pickup, Red for dropoff
# Pydeck map with an arrow between pickup and dropoff locations
layer = pdk.Layer(
    "LineLayer",
    data=pd.DataFrame(
        {"start_lat": [pickup_latitude], "start_lon": [pickup_longitude],
         "end_lat": [dropoff_latitude], "end_lon": [dropoff_longitude]}
    ),
    get_source_position=["start_lon", "start_lat"],
    get_target_position=["end_lon", "end_lat"],
    get_width=5,
    get_color=[255, 0, 0],  # Red arrow
    pickable=False,
)

# Render the map
st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=(pickup_latitude + dropoff_latitude) / 2 if pickup_latitude and dropoff_latitude else 40.7,
            longitude=(pickup_longitude + dropoff_longitude) / 2 if pickup_longitude and dropoff_longitude else -74.0,
            zoom=12,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=map_data,
                get_position=["lon", "lat"],
                get_color="colour",  # Blue markers
                get_radius=100,
            ),
            layer,
        ],
    )
)
# def get_map_data():

#     data = {
#         'pickup_latitude': pickup_latitude,
#         'pickup_longitude': pickup_longitude
#     }
#     return pd.DataFrame(data,
#             columns=['lat', 'lon']
#         )

# df = get_map_data()

# st.map(df)

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

# '''

# 2. Let's build a dictionary containing the parameters for our API...

# 3. Let's call our API using the `requests` package...

# 4. Let's retrieve the prediction from the **JSON** returned by the API...

# ## Finally, we can display the prediction to the user
# '''
