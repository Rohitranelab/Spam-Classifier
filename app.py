import streamlit as st
import pickle
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import nltk
import string

ps = PorterStemmer()

tfidf = pickle.load(open('artifact\\vectorizer.pkl', 'rb'))
model = pickle.load(open('artifact\\model.pkl', 'rb'))

def transform_text(text):
    text = text.lower()

    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))
            
    return " ".join(y)


# ---------------- UI ----------------

st.set_page_config(
    page_title="Spam Classifier",
    page_icon="📩",
    layout="centered"
)

st.title("📩 Email / SMS Spam Classifier")
st.caption("Check whether a message is Spam or Not Spam using NLP + ML")

input = st.text_area('✉️ Enter the message below:', height=150, placeholder="Type or paste a message here...")

col1, col2 = st.columns([1, 1])
with col1:
    predict_clicked = st.button('🔍 Predict', use_container_width=True)
with col2:
    clear_clicked = st.button('🗑️ Clear', use_container_width=True)

if clear_clicked:
    st.rerun()

if predict_clicked:
    if not input.strip():
        st.warning("⚠️ Please enter a message before predicting.")
    else:
        with st.spinner('Analyzing message...'):
            transformed_data = transform_text(input)
            vector_input = tfidf.transform([transformed_data])
            result = model.predict(vector_input)[0]

        st.markdown("### Result:")
        if result == 1:
            st.error("🚫 SPAM")
        else:
            st.success("✅ NOT SPAM")