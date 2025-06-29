# ==================== app.py (FINAL CLEAN VERSION, READY TO RUN) ====================

import streamlit as st
import base64
import joblib
import requests
from newspaper import Article
from datetime import datetime
import time
from streamlit_option_menu import option_menu

# ==================== Page Configuration ====================
st.set_page_config(
    page_title="Fake News Detector",
    layout="wide"
)

# ==================== CSS Styling ====================

st.markdown("""
    <style>
    div.stButton > button {
        color: white !important;
        background-color: #e63946 !important;
        border: none;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-size: 16px;
    }
    div.stButton > button:hover {
        background-color: #d62828 !important;
    }
    .stTextInput, .stTextArea, .stSelectbox, .stMultiSelect,
    .stSlider, .stDateInput, .stTimeInput, .stCheckbox, .stRadio, .stFileUploader {
        background-color: rgba(0,0,0,0) !important;
        color: white !important;
    }
    ::placeholder {
        color: rgba(255, 255, 255, 0.7);
    }
    .title {
        font-size: 36px;
        font-weight: bold;
        color: white;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 20px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== Background ====================
def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as img:
            encoded_string = base64.b64encode(img.read()).decode()
        st.markdown(f"""
            <style>
            .stApp {{
                background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
                            url(data:image/jpeg;base64,{encoded_string});
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
            </style>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ Background image not found. Please add 'background.jpeg'.")

add_bg_from_local('background.jpeg')

# ==================== Load Model ====================
try:
    vectorizer = joblib.load("vectorizer.jb")
    model = joblib.load("lr_model.jb")
except Exception as e:
    st.error(f"❌ Failed to load model/vectorizer: {e}")
    st.stop()

# ==================== API Key ====================
api_key = "9e015eb74bbe5511699840795cf8058e"

# ==================== Navigation ====================
selected = option_menu(
    menu_title=None,
    options=["Home", "Check News by Keyword", "Check News by Entering Text"],
    icons=["house", "search", "pencil"],
    orientation="horizontal",
    default_index=0,
    styles={
        "container": {"padding": "0!important", "background-color": "#000000"},
        "icon": {"color": "#e63946", "font-size": "24px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "0px", "color": "white", "--hover-color": "#333"},
        "nav-link-selected": {"background-color": "#e63946", "color": "white"},
    }
)

page = selected

# ==================== Real/Fake Label Box ====================
def show_label(prediction):
    if prediction == 1:
        st.markdown("""
            <div style="
                border: 2px solid #00FF00;
                border-radius: 8px;
                padding: 10px;
                color: #00FF00;
                font-weight: bold;
                text-align: center;
                background-color: rgba(0, 255, 0, 0.1);
                ">
                ✅ Predicted as Real News
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="
                border: 2px solid #FF4C4C;
                border-radius: 8px;
                padding: 10px;
                color: #FF4C4C;
                font-weight: bold;
                text-align: center;
                background-color: rgba(255, 76, 76, 0.1);
                ">
                🚩 Predicted as Fake News
            </div>
        """, unsafe_allow_html=True)

# ==================== Home Page ====================
if page == "Home":
    st.markdown('<div class="title">📰 Live News Monitoring</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">View real-time predictions for the latest news articles</div>', unsafe_allow_html=True)

    auto_refresh = st.checkbox("🔄 Auto Refresh every 60 seconds")
    if auto_refresh:
        st.info("Auto-refreshing every 60 seconds. Uncheck to stop.")
        time.sleep(60)
        st.rerun()

    if st.button("Fetch Latest News & Predict"):
        url = f"https://gnews.io/api/v4/top-headlines?lang=en&country=in&max=6&apikey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            if articles:
                cols = st.columns(3)
                for idx, article in enumerate(articles):
                    with cols[idx % 3]:
                        st.image(article.get('image'), width=250)
                        st.write(f"**{article.get('title')}**")
                        st.write(f"**Published:** {article.get('publishedAt', 'Unknown')}")

                        text = (article.get('description') or '') + ' ' + (article.get('content') or '')
                        if text.strip():
                            prediction = model.predict(vectorizer.transform([text]))
                            show_label(prediction[0])
                        else:
                            st.warning("⚠️ No content to analyze.")
                        st.markdown("---")
            else:
                st.warning("⚠️ No articles found. Please try again later.")
        else:
            st.error(f"❌ Error fetching articles: {response.status_code}")
 # Check News from URL
    st.markdown("---")
    st.header("🌐 Check News from a URL")

    def extract_text_from_url(url):
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.title, article.text
        except Exception as e:
            st.error(f"❌ Failed to extract: {e}")
            return None, None

    news_url = st.text_input("Paste a news article URL:")
    if st.button("Check This URL"):
        if news_url.strip():
            title, text = extract_text_from_url(news_url.strip())
            if text:
                st.markdown(f"### 📰 {title}")
                st.write(text[:500] + "..." if len(text) > 500 else text)
                prediction = model.predict(vectorizer.transform([text]))
                if text.strip():
                            prediction = model.predict(vectorizer.transform([text]))
                            show_label(prediction[0])
            else:
                st.warning("⚠️ Could not extract text from URL.")
        else:
            st.warning("⚠️ Please enter a valid URL.")

# ==================== Check by Keyword ====================
elif page == "Check News by Keyword":
    st.markdown('<div class="title">🔍 Check News by Keyword</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Fetch news by keyword and detect fake news.</div>', unsafe_allow_html=True)

    keyword = st.text_input("Enter keyword/topic:")
    if st.button("Fetch News & Analyze"):
        if keyword.strip():
            url = f"https://gnews.io/api/v4/search?q={keyword}&lang=en&country=in&max=5&apikey={api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                articles = response.json().get("articles", [])
                if articles:
                    for idx, article in enumerate(articles, 1):
                        st.markdown(f"### 📰 Article {idx}: {article['title']}")
                        st.markdown(f"[Read Full Article]({article['url']})")
                        text = (article.get('description') or '') + ' ' + (article.get('content') or '')
                        if text.strip():
                            prediction = model.predict(vectorizer.transform([text]))
                            show_label(prediction[0])
                        else:
                            st.warning("⚠️ No content found to analyze.")
                        st.markdown("---")
                else:
                    st.warning("⚠️ No articles found for this keyword. Please try different keywords.")
            else:
                st.error(f"❌ Error fetching articles: {response.status_code}")
        else:
            st.warning("⚠️ Please enter a keyword.")

# ==================== Check by Entering Text ====================
elif page == "Check News by Entering Text":
    st.markdown('<div class="title">✍️ Check News by Entering Text</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Paste or type an article to check if it is real or fake.</div>', unsafe_allow_html=True)

    text_input = st.text_area("Paste your news article here:")
    if st.button("Check News"):
        if text_input.strip():
            if len(text_input.split()) < 20:
                st.warning("⚠️ The entered text is very short. Please enter the full content for better accuracy.")
            prediction = model.predict(vectorizer.transform([text_input]))
            show_label(prediction[0])
        else:
            st.warning("⚠️ Please enter text to analyze.")

# ==================== END ====================
