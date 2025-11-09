import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import ast
import seaborn as sns

# PAGE CONFIG
st.set_page_config(page_title="🏠 Real Estate Analysis", page_icon="📊", layout="wide")

# Apply dark theme for matplotlib & seaborn
plt.style.use("dark_background")
sns.set_theme(style="darkgrid")

# ========= HEADER =========
st.title("🏠 Real Estate Analytics Dashboard")
st.markdown("A modern interactive dashboard to explore **real estate data** 📈")

# ========= LOAD DATA =========
new_df = pd.read_csv('Dataset/data_visz1.csv')
word_cloud = pd.read_csv('Dataset/wordcloud.csv')

# ========= GEO MAP =========
st.subheader("🌍 Sector Price per Sqft Geo Map")

mean_df = new_df.groupby('sector')[['price','price_per_sqft','built_up_area','latitude','longitude']].mean()

# fig_map = px.scatter_map(
#     mean_df,
#     lat="latitude", lon="longitude",
#     color="price_per_sqft", size="built_up_area",
#     color_continuous_scale=px.colors.cyclical.IceFire,
#     zoom=10, map_style="open-street-map",
#     hover_name=mean_df.index,
#     width=1000, height=600
# )

fig_map = px.scatter_mapbox(
    mean_df,
    lat="latitude", lon="longitude",
    color="price_per_sqft", size="built_up_area",
    color_continuous_scale=px.colors.cyclical.IceFire,
    zoom=10, mapbox_style="carto-darkmatter",
    hover_name=mean_df.index,
    width=1000, height=600
)

st.plotly_chart(fig_map, use_container_width=True)

# ========= TABS =========
tab1, tab2, tab3, tab4 = st.tabs(["☁️ Amenities WordCloud", "📊 Area vs Price", "🥧 BHK Distribution", "📦 Price Comparisons"])

# ========= WORDCLOUD =========
with tab1:
    st.subheader("☁️ Sector-wise Amenities WordCloud")

    sector_list = ["Overall"] + sorted(word_cloud['sector'].dropna().unique().tolist())
    selected_sector = st.selectbox("Choose a Sector", sector_list, key="wordcloud_sector")

    if selected_sector == "Overall":
        sector_features = word_cloud['features']
    else:
        sector_features = word_cloud.loc[word_cloud['sector'] == selected_sector, 'features']

    main_list = []
    for item in sector_features.dropna().apply(ast.literal_eval):
        main_list.extend(item)

    if main_list:
        feature_text = ' '.join(main_list)
        wordcloud = WordCloud(
            width=800, height=800,
            background_color="black", colormap="viridis",
            stopwords=set(['s']),
            min_font_size=12
        ).generate(feature_text)

        fig_wc, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig_wc)
    else:
        st.warning("⚠️ No amenities data available for this sector.")

# ========= AREA VS PRICE =========
with tab2:
    st.subheader("📊 Area vs Price Analysis")

    property_type = st.radio("Choose Property Type:", ["flat", "house"], horizontal=True)
    df_filtered = new_df[new_df['property_type'] == property_type]

    fig1 = px.scatter(
        df_filtered, x="built_up_area", y="price",
        color="bedRoom", title=f"Area vs Price in {property_type.capitalize()}",
        labels={"built_up_area":"Built-Up Area", "price":"Price"},
        color_continuous_scale="Plotly3", template="plotly_dark"
    )
    st.plotly_chart(fig1, use_container_width=True)

# ========= BHK PIE =========
with tab3:
    st.subheader("🥧 BHK Distribution by Sector")

    sector_option = ["Overall"] + sorted(new_df['sector'].unique().tolist())
    selected_sector = st.selectbox("Select Sector", sector_option, key="pie_sector")

    if selected_sector == "Overall":
        fig2 = px.pie(new_df, names="bedRoom", title="Overall BHK Distribution", template="plotly_dark")
    else:
        fig2 = px.pie(new_df[new_df['sector'] == selected_sector], names="bedRoom", title=f"BHK Distribution in {selected_sector}", template="plotly_dark")

    st.plotly_chart(fig2, use_container_width=True)

# ========= PRICE COMPARISONS =========
with tab4:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💰 Side by Side BHK Price Comparison")
        fig3 = px.box(new_df[new_df['bedRoom'] <= 5], x="bedRoom", y="price",
                      title="BHK Price Range", template="plotly_dark")
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.subheader("🏠 Price Distribution by Property Type")
        fig4 = plt.figure(figsize=(8, 4))
        sns.kdeplot(new_df[new_df['property_type'] == 'house']['price'], label="House", fill=True)
        sns.kdeplot(new_df[new_df['property_type'] == 'flat']['price'], label="Flat", fill=True)
        plt.legend()
        st.pyplot(fig4)

st.markdown("---")
st.markdown("🔎 *Dashboard built with Streamlit, Plotly & Seaborn in Dark Mode* 🚀")
