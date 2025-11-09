import streamlit as st
import pickle
import pandas as pd

# ----------------------------
# Streamlit Page Config
# ----------------------------
st.set_page_config(
    page_title="🏘️ Smart Apartment Recommender",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Load Data
# ----------------------------
df=pickle.load(open("Dataset/appartments.pkl", "rb"))
location_df = pickle.load(open("Dataset/location_distance.pkl", "rb"))
location_df_normalized = pickle.load(open("Dataset/nomalized_location.pkl", "rb"))

similarity = pickle.load(open("Dataset/cosine_similarity_1", "rb"))
similarity_2 = pickle.load(open("Dataset/cosine_similarity_2", "rb"))
similarity_3 = pickle.load(open("Dataset/cosine_similarity_3", "rb"))

# renaming the column
df=df.rename(columns={'PropertyName':'Property Name'})

# ----------------------------
# Recommendation Function
# ----------------------------
def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 30*similarity + 20*similarity_2 + 8*similarity
    
    sim_scores = list(enumerate(cosine_sim_matrix[location_df_normalized.index.get_loc(property_name)]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n+1]]
    
    top_properties = location_df_normalized.index[top_indices].tolist()
    
    recommendations_df = pd.DataFrame({
        'Property Name': top_properties,
        'SimilarityScore': top_scores
    })
    
    # Merge links
    recommendations_df = recommendations_df.merge(
        df[['Property Name', 'Link']], on='Property Name', how='left'
    )
    
    # Add clickable markdown links
    recommendations_df['Link'] = recommendations_df['Link'].apply(
        lambda x: f'<a href="{x}" target="_blank">LINK</a>' if pd.notnull(x) else "No Link"
    )
    
    return recommendations_df

# ----------------------------
# Sidebar Filters
# ----------------------------
with st.sidebar:
    st.header("⚙️ Search Settings")
    selected_location = st.selectbox("📍 Select your Location", sorted(location_df.columns.to_list()))
    radius = st.number_input("📏 Distance in KMs", min_value=1, max_value=1000, value=5)

    if st.button("🔎 Search Nearby"):
        result = location_df[location_df[selected_location] <= radius * 1000][selected_location].sort_values()
        if result.empty:
            st.warning("⚠️ No property is around the given range.")
            st.session_state["search_results"] = None
        else:
            appartment = [f"{key} : {round(value/1000)} kms" for key, value in result.items()]
            st.session_state["search_results"] = appartment

# ----------------------------
# Main UI
# ----------------------------
st.title("🏘️ Smart Apartment Recommender")
st.markdown("---")

# Show search results
if "search_results" in st.session_state and st.session_state["search_results"]:
    st.subheader("📍 Properties Near You")
    selected_appt = st.radio(
        "Select a property from the results:",
        st.session_state["search_results"],
        key="selected_appt"
    )

    if st.button("✨ Show Recommendations"):
        selected_property = st.session_state["selected_appt"].split(":")[0].strip()
        st.success(f"✅ You selected: **{selected_property}**")

        # Recommendations
        st.subheader("🏡 Top 5 Recommended Properties")
        recommendations = recommend_properties_with_scores(selected_property)
        # Apply CSS for wide table
        st.markdown(
            """
            <style>
            table {
                width: 100% !important;
                border-collapse: collapse;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #444;
            }
            th {
                background-color: #222;
                color: #fff;
            }
            tr:hover {
                background-color: #333;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Show styled table
        st.markdown(recommendations.to_html(escape=False, index=False), unsafe_allow_html=True)
        # for i, row in recommendations.iterrows():
        #     with st.expander(f"🏠 {row['PropertyName']}"):
        #         st.write(f"🔗 Match Score: {row['SimilarityScore']:.4f}")
        #         st.progress(min(max(row["SimilarityScore"], 0), 1))  # Show score as progress bar
        #         st.caption(f"🔗 Match Strength: {round(row['SimilarityScore']*100)}%")
        #         st.markdown("---")
