# 📰 Fake News Detection Streamlit App

A **deployed, interactive, real-time Fake News Detection app** using **Machine Learning and Streamlit**, allowing users to verify news articles by URL, keyword, or manual entry while providing an engaging and intuitive UI.

---

## 🚀 Project Overview

The widespread circulation of fake news can have serious social consequences. This project aims to **detect and classify fake news articles in real-time** by leveraging a **Logistic Regression model with TF-IDF vectorization**, wrapped in an interactive **Streamlit dashboard**.

The app can:
- Fetch live news articles using **GNews API**.
- Allow users to verify news by:
  - Live monitoring latest headlines.
  - Checking news by entering keywords.
  - Checking news by pasting text.
- Predict whether a news article is *real* or *fake* instantly.
- Display a clean, dark-themed UI for readability.

---

## 🎯 Features

✅ **Real-Time News Monitoring**  
✅ **Check News by URL, Keyword, or Text Entry**  
✅ **Fake vs. Real Prediction using Trained ML Model**  
✅ **Clean, Dark-Themed, Responsive UI**  
✅ **Fully Local or Deployable on Streamlit Cloud**

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** (UI)
- **scikit-learn** (ML Model - Logistic Regression)
- **Newspaper3k** (Text extraction from URLs)
- **GNews API** (Live News Fetching)
- **Joblib** (Model Serialization)

---

## 🤖 Model Details

- **Vectorizer:** TF-IDF Vectorizer (`vectorizer.jb`)
- **Classifier:** Logistic Regression (`lr_model.jb`)
- **Training:** Trained on a labeled dataset of fake and real news articles.

---

## 📸 Screenshots

| Dashboard | 
|----------|
| ![Dashboard](homepage.png) |

| Get News By Entering Keyword | Get News by Entering Texts or Few Sentences |
|----------|-----------|
| ![Get News By Entering Keyword](newsbykeyword.png) | ![Get News by Entering Texts or Few Sentences](newsbyenteringtext.png) |

| Prediction(by a URL) | Prediction(by the Keywords) |
|----------|-----------|
| ![Prediction(by a URL)](prediction(byURL).png) | ![Prediction(by the Keywords](prediction(bykeyword).png) |

---

## ⚡ Installation and Running Locally

1️⃣ **Clone the repository:**

```bash
git clone https://github.com/yourusername/fake-news-detection-app.git
cd fake-news-detection-app
```
2️⃣ Create and activate a virtual environment:

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```
3️⃣ Install dependencies:

```bash
pip install -r requirements.txt
```
4️⃣ Run the Streamlit app:

```bash
streamlit run app.py
```
