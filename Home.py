import streamlit as st

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="🏡 Real Estate Intelligence",
    page_icon="🏠",
    layout="wide"
)

# ================== HERO SECTION ==================
st.markdown(
    """
    <style>
        .main {
            background-color: #0e1117;
            color: white;
        }
        .hero-title {
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            color: #f9f9f9;
        }
        .hero-subtitle {
            font-size: 20px;
            text-align: center;
            color: #bbb;
            margin-bottom: 30px;
        }
        .card {
            background-color: #161a23;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.4);
            transition: 0.3s;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.6);
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 14px;
            color: #aaa;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="hero-title">🏡 Real Estate Intelligence App</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Price Prediction | Market Analytics | Smart Recommendations</p>', unsafe_allow_html=True)

st.write("")
st.write("")

# ================== NAVIGATION CARDS ==================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">💰</div>', unsafe_allow_html=True)
    if st.button("Go to Price Prediction", key="btn1"):
        st.switch_page("pages/Price Predicter.py")

with col2:
    st.markdown('<div class="card">📊</div>', unsafe_allow_html=True)
    if st.button("Go to Analytics Dashboard", key="btn2"):
        st.switch_page("pages/Analysis.py")

with col3:
    st.markdown('<div class="card">🏘️</div>', unsafe_allow_html=True)
    if st.button("Go to Recommender System", key="btn3"):
        st.switch_page("pages/Recommendations.py")

st.write("")
st.write("---")

# ================== HOW TO USE ==================
st.subheader("🛠️ How to Use")
st.markdown(
    """
    - Select a module from above  
    - Provide property/location details  
    - Get insights instantly ⚡  
    - Explore recommendations & predictions
    """
)

# ================== FOOTER ==================
st.markdown('<p class="footer">👨‍💻 Developed by <b>ANUJ BISHT</b> | 🚀 Powered by Streamlit</p>', unsafe_allow_html=True)
