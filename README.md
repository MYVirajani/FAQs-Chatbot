# AI FAQ Chatbot

An NLP-powered FAQ chatbot that matches user questions to the most relevant answer using **TF-IDF vectorization** and **cosine similarity**. Built with Python, NLTK, scikit-learn, and Streamlit.


## 🗂️ Project Structure

```
FAQs-Chatbot/
├── app.py           
├── chatbot.py       
├── faqs.py          
└── requirements.txt
```

---

## ⚙️ How It Works

```
User Input
    │
    ▼
Preprocessing (lowercase → remove punctuation → tokenize → remove stopwords → lemmatize)
    │
    ▼
TF-IDF Vectorization
    │
    ▼
Cosine Similarity (against all FAQ questions)
    │
    ▼
Best Match (if confidence ≥ threshold) → Return Answer
    │
    └── Below threshold → Return fallback message
```

### NLP Pipeline

| Step | Description |
|---|---|
| Lowercasing | Normalize text case |
| Punctuation removal | Remove non-word characters |
| Tokenization | Split text into words |
| Stopword removal | Remove common words (the, is, a…) |
| Lemmatization | Reduce words to base form (running → run) |

### Matching

- All FAQ questions are vectorized using **TF-IDF** at startup
- User query is preprocessed and vectorized using the same vectorizer
- **Cosine similarity** scores are computed against all FAQ vectors
- The highest-scoring match above the confidence threshold is returned

---

## ▶️ How to run

### 1. Clone the Repository

```bash
git clone https://github.com/MYVirajani/FAQs-Chatbot
cd FAQs-Chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
streamlit run app.py
```

---



---

## 🖥️ Example Interaction

| User Input | Matched FAQ | Confidence |
|---|---|---|
| "What is machine learning?" | "What is machine learning?" | 100% |
| "How does AI differ from ML?" | "What is the difference between AI and ML?" | 82% |
| "explain neural networks" | "What is a neural network?" | 100% |
| "what's the weather today?" | — | ❌ I'm sorry, I don't have an answer for that question. Try rephrasing, or ask something about AI & Machine Learning! |



