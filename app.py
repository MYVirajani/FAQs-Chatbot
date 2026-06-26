import streamlit as st
from chatbot import get_response
from faqs import FAQS

st.set_page_config(
    page_title="AI FAQ Chatbot",
    layout="centered",
)

st.markdown("""
<style>
    .stApp { background-color: #0f1117; }

    .chat-container {
        max-width: 720px;
        margin: 0 auto;
    }

    .user-msg {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: #fff;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0 8px 15%;
        font-size: 0.95rem;
        line-height: 1.5;
        box-shadow: 0 2px 8px rgba(99,102,241,0.3);
    }

    .bot-msg {
        background: #1e2030;
        color: #e2e8f0;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 15% 8px 0;
        font-size: 0.95rem;
        line-height: 1.5;
        border: 1px solid #2d3150;
    }

    .confidence {
        font-size: 0.72rem;
        color: #6b7280;
        margin-top: 4px;
        margin-left: 4px;
    }

    .matched-q {
        font-size: 0.78rem;
        color: #818cf8;
        font-style: italic;
        margin-top: 6px;
    }

    h1 { color: #a5b4fc !important; letter-spacing: -0.5px; }
    .subtitle { color: #6b7280; font-size: 0.9rem; margin-top: -12px; margin-bottom: 24px; }

    .stTextInput > div > div > input {
        background: #1e2030;
        border: 1px solid #374151;
        color: #e2e8f0;
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 0.95rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 2px rgba(99,102,241,0.2);
    }

    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 28px;
        font-weight: 600;
        width: 100%;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.9; }

    hr { border-color: #1e2030; }
</style>
""", unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "bot",
        "text": "Hi! I'm your **AI & Machine Learning FAQ Bot**. "
                "Ask me anything about AI, ML, deep learning, NLP, and more!",
        "meta": None,
    })

if "input_key" not in st.session_state:
    st.session_state.input_key = 0


def handle_send():
    user_text = st.session_state.get(f"input_box_{st.session_state.input_key}", "").strip()
    if not user_text:
        return
    st.session_state.messages.append({"role": "user", "text": user_text, "meta": None})
    result = get_response(user_text)
    st.session_state.messages.append({
        "role": "bot",
        "text": result["answer"],
        "meta": result,
    })
    st.session_state.input_key += 1  


st.markdown("## AI FAQ Chatbot")
st.markdown("---")


for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg"> {msg["text"]}</div>',
                    unsafe_allow_html=True)
    else:
        html = f'<div class="bot-msg"> {msg["text"]}'
        if msg.get("meta") and msg["meta"]["found"]:
            conf = int(msg["meta"]["confidence"] * 100)
            html += f'<div class="confidence">Confidence: {conf}%</div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)


st.markdown("---")
col1, col2 = st.columns([5, 1])
with col1:
    st.text_input(
        "Your question",
        placeholder="e.g. What is machine learning?",
        label_visibility="collapsed",
        key=f"input_box_{st.session_state.input_key}",
        on_change=handle_send,  
    )
with col2:
    st.button("Send", on_click=handle_send)  


with st.sidebar:
    st.markdown("### Browse All FAQs")
    st.markdown("Click a question to copy and ask it!")
    st.markdown("---")
    for i, faq in enumerate(FAQS, 1):
        with st.expander(f"Q{i}: {faq['question'][:24]}..."):
             st.markdown(f"**Q:** {faq['question']}")

    st.markdown("---")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()