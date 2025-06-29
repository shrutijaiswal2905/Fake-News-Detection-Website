import streamlit as st
import joblib
import requests
from newspaper import Article
import time

# Load model and vectorizer
vectorizer = joblib.load("vectorizer.jb")
model = joblib.load("lr_model.jb")

# Sidebar Navbar
page = st.sidebar.radio("Navigation", [
    "🏠 Home",
    "🔍 Check News by Keyword",
    "✍️ Check News by Entering Text"
])

# API Key for GNews
api_key = "9e015eb74bbe5511699840795cf8058e"  # Replace with your key

# ---------- HOME PAGE ----------
if page == "🏠 Home":
    st.title("📰 Live News Monitoring: Real-Time Predictions")
    auto_refresh = st.checkbox("🔄 Auto Refresh every 60 seconds")

    if auto_refresh:
        st.info("Auto-refreshing every 60 seconds... Stop it anytime by unchecking above.")
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
                        st.write(f"Published: {article.get('publishedAt')}")
                        
                        text_to_analyze = (article.get('description') or "") + " " + (article.get('content') or "")
                        if text_to_analyze.strip():
                            transform_input = vectorizer.transform([text_to_analyze])
                            prediction = model.predict(transform_input)
                            if prediction[0] == 1:
                                st.success("✅ Predicted as Real News")
                            else:
                                st.error("🚩 Predicted as Fake News")
                        else:
                            st.warning("⚠️ No content found to analyze.")
                        st.markdown("---")
            else:
                st.warning("⚠️ No articles fetched from GNews.")
        else:
            st.error(f"Error fetching articles: {response.status_code}")

    # ---- Check News from URL Section ----
    st.markdown("---")
    st.header("🌐 Check News from a URL")
    def extract_text_from_url(url):
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.title, article.text
        except Exception as e:
            st.error(f"Failed to extract article: {e}")
            return None, None

    news_url = st.text_input("Paste a news article URL:")

    if st.button("Check This URL"):
        if news_url.strip():
            title, text = extract_text_from_url(news_url.strip())
            if text:
                st.markdown(f"### 📰 {title}")
                st.write(text[:500] + "..." if len(text) > 500 else text)

                transform_input = vectorizer.transform([text])
                prediction = model.predict(transform_input)

                if prediction[0] == 1:
                    st.success("✅ This News is Real!")
                else:
                    st.error("🚩 This News is Fake!")
            else:
                st.warning("⚠️ Could not extract text from the provided URL.")
        else:
            st.warning("⚠️ Please paste a valid URL.")

# ---------- CHECK NEWS BY KEYWORD PAGE ----------
elif page == "🔍 Check News by Keyword":
    st.title("🔍 Check News by Keyword")
    st.write("Fetch live Indian news articles by keyword and detect fake news.")

    def fetch_articles_from_gnews(query, api_key):
        url = f"https://gnews.io/api/v4/search?q={query}&lang=en&country=in&max=5&apikey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            return articles
        else:
            st.error(f"Error fetching articles: {response.status_code}")
            return []

    search_query = st.text_input("Enter a news topic or keyword:")

    if st.button("Fetch News & Analyze"):
        if search_query.strip():
            articles = fetch_articles_from_gnews(search_query.strip(), api_key)
            if articles:
                for idx, article in enumerate(articles, start=1):
                    st.markdown(f"### 📰 Article {idx}: {article['title']}")
                    st.markdown(f"[Read Full Article]({article['url']})")

                    text_to_analyze = (article.get('description') or "") + " " + (article.get('content') or "")
                    if text_to_analyze.strip():
                        transform_input = vectorizer.transform([text_to_analyze])
                        prediction = model.predict(transform_input)

                        if prediction[0] == 1:
                            st.success("✅ This News is Real!")
                        else:
                            st.error("🚩 This News is Fake!")
                    else:
                        st.warning("⚠️ No content found to analyze.")
            else:
                st.warning("⚠️ No articles found for this keyword.")
        else:
            st.warning("⚠️ Please enter a topic to search.")

# ---------- CHECK NEWS BY ENTERING TEXT PAGE ----------
elif page == "✍️ Check News by Entering Text":
    st.title("✍️ Check News by Entering Text")
    inputn = st.text_area("Enter the news article content here:")

    if st.button("Check News"):
        if inputn.strip():
            if len(inputn.split()) < 20:
                st.warning("⚠️ The entered text is very short. For better accuracy, please enter the *full news content*, not just the headline.")
            transform_input = vectorizer.transform([inputn])
            prediction = model.predict(transform_input)

            if prediction[0] == 1:
                st.success("✅ The News is Real!")
            else:
                st.error("🚩 The News is Fake!")
        else:
            st.warning("⚠️ Please enter some text to analyze.")
