import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from faqs import FAQS

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('punkt_tab', quiet=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


def preprocess(text: str) -> str:
    """Tokenize, lowercase, remove stopwords and punctuation, then lemmatize."""
    tokens = nltk.word_tokenize(text.lower())
    tokens = [t for t in tokens if t not in string.punctuation]
    tokens = [t for t in tokens if t not in stop_words]
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(tokens)


faq_questions = [faq["question"] for faq in FAQS]
faq_answers   = [faq["answer"]   for faq in FAQS]
processed_questions = [preprocess(q) for q in faq_questions]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(processed_questions)

THRESHOLD = 0.15  

def get_response(user_input: str) -> dict:
    """
    Match user input against FAQs using TF-IDF + cosine similarity.

    Returns a dict with:
      - answer: the best matching answer (or fallback message)
      - matched_question: the FAQ question that was matched
      - confidence: similarity score (0–1)
      - found: bool
    """
    processed_input = preprocess(user_input)
    input_vec = vectorizer.transform([processed_input])
    similarities = cosine_similarity(input_vec, tfidf_matrix).flatten()

    best_idx   = similarities.argmax()
    best_score = similarities[best_idx]

    if best_score < THRESHOLD:
        return {
            "answer": "I'm sorry, I don't have an answer for that question. "
                      "Try rephrasing, or ask something about AI & Machine Learning!",
            "matched_question": None,
            "confidence": float(best_score),
            "found": False,
        }

    return {
        "answer": faq_answers[best_idx],
        "matched_question": faq_questions[best_idx],
        "confidence": float(best_score),
        "found": True,
    }