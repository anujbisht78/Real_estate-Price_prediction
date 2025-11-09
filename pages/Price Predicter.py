import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os
import gdown


# PAGE CONFIG

st.set_page_config(
    page_title="Real Estate Price Prediction",
    page_icon="🏠",
    layout="wide"
)


# LOAD DATA & MODEL

# @st.cache_resource
# def load_data_and_model():
#     with open('df.pkl', 'rb') as file:
#         df = pickle.load(file)

#     with open('pipeline.pkl', 'rb') as file:
#         pipeline = pickle.load(file)

#     return df, pipeline

# df, pipeline = load_data_and_model()

# Google Drive file ID for your pipeline.pkl
# Direct Google Drive link to your pipeline.pkl file
DRIVE_URL = "https://drive.google.com/uc?id=1pZ3Bue_ezfRnt_3DRTLvvi_9RBK40Qae"
MODEL_PATH = "pipeline.pkl"

@st.cache_resource
def load_data_and_model():
    # Load local DataFrame
    with open('df.pkl', 'rb') as file:
        df = pickle.load(file)

    # Download model if not found locally
    if not os.path.exists(MODEL_PATH):
        st.info("📦 Downloading model from Google Drive... please wait ⏳")
        try:
            gdown.download(DRIVE_URL, MODEL_PATH, quiet=False)
            st.success("✅ Model downloaded successfully!")
        except Exception as e:
            st.error(f"❌ Failed to download model: {e}")
            st.stop()

    # Load trained pipeline
    with open(MODEL_PATH, 'rb') as file:
        pipeline = pickle.load(file)

    return df, pipeline

# Load data and model
df, pipeline = load_data_and_model()


# HEADER

st.title("🏡 Real Estate Price Estimator")
st.markdown("Enter property details below to estimate the **price range** in Crores.")


# USER INPUTS

st.sidebar.header("🔑 Property Details")

property_type = st.sidebar.selectbox('Property Type', ['flat', 'house'])
sector = st.sidebar.selectbox('Sector', sorted(df['sector'].unique().tolist()))
bedroom = float(st.sidebar.selectbox('Bedrooms', sorted(df['bedRoom'].unique().tolist())))
bathroom = float(st.sidebar.selectbox('Bathrooms', sorted(df['bathroom'].unique().tolist())))
balcony = st.sidebar.selectbox('Balconies', sorted(df['balcony'].unique().tolist()))
property_age = st.sidebar.selectbox('Property Age', df['agePossession'].unique())
built_up_area = float(st.sidebar.number_input('Built-up Area (sq.ft.)', min_value=200.0, max_value=10000.0, step=50.0))
servant_room = float(st.sidebar.radio('Servant Room', [0.0, 1.0]))
store_room = float(st.sidebar.radio('Store Room', [0.0, 1.0]))
furnishing_type = st.sidebar.selectbox('Furnishing Type', df['furnishing_type'].unique().tolist())
luxury_category = st.sidebar.selectbox('Luxury Category', df['luxury_category'].unique().tolist())
floor_category = st.sidebar.selectbox('Floor Category', df['floor_category'].unique().tolist())


# PREDICTION

if st.sidebar.button("🔮 Predict Price"):

    # Prepare input
    data = [[property_type, sector, bedroom, bathroom, balcony,
             property_age, built_up_area, servant_room, store_room,
             furnishing_type, luxury_category, floor_category]]

    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']

    one_df = pd.DataFrame(data, columns=columns)

    # Prediction
    try:
        base_price = np.expm1(pipeline.predict(one_df))[0]
        low, high = base_price - 0.22, base_price + 0.22

        
        # OUTPUT DISPLAY
        
        st.success("✅ Prediction Successful!")

        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Estimated Price (Low)", f"{round(low, 2)} Cr")
        col2.metric("💰 Estimated Price (High)", f"{round(high, 2)} Cr")
        col3.metric("🏷️ Mid Estimate", f"{round(base_price, 2)} Cr")

        with st.expander("📊 Input Summary"):
            st.dataframe(one_df)

    except Exception as e:
        st.error(f"⚠️ Prediction failed: {e}")
