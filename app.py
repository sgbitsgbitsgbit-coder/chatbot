# app.py (Stunning UI - No streamlit_chat needed)
import os
import streamlit as st
from google import genai

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Gemini AI Chat",
    page_icon="🤖",
    layout="wide"
)

# -------------------------
# Sidebar (API Key + Settings)
# -------------------------
st.sidebar.title("⚙️ Settings")
api_key = st.sidebar.text_input("🔑 Enter API Key", type="password")

if not api_key:
    st.sidebar.warning("No API key provided. Please enter one above.")
    client = None
else:
    client = genai.Client(api_key=api_key)
    st.sidebar.success("✅ API key added")

model_name = st.sidebar.selectbox(
    "🤖 Choose Gemini Model",
    ["gemini-2.5-flash", "gemini-2.0-pro-exp-02-05", "gemini-1.5-pro"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 Tip: Ask creative or complex questions!")

# -------------------------
# Custom CSS for Stunning UI
# -------------------------
st.markdown(
    """
    <style>
    /* Background */
    .stApp {
        background: linear-gradient(135deg, #1f1c2c, #928DAB);
        color: white;
    }

    /* Title */
    h1, h2, h3 {
        text-align: center;
        color: #00f5d4 !important;
    }

    /* Prompt input */
    textarea {
        border-radius: 12px !important;
        border: 2px solid #00f5d4 !important;
        padding: 12px;
        font-size: 1.1rem !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: #00f5d4 !important;
        color: black !important;
        border-radius: 12px;
        font-weight: bold;
        font-size: 1.1rem;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #06d6a0 !important;
        transform: scale(1.05);
    }

    /* Chat bubbles */
    .chat-bubble {
        border-radius: 12px;
        padding: 12px 16px;
        margin: 10px 0;
        font-size: 1.05rem;
        line-height: 1.4;
    }
    .chat-bubble.user {
        background-color: #00f5d4;
        color: black;
        text-align: right;
    }
    .chat-bubble.bot {
        background-color: #222;
        color: #f5f5f5;
        border: 1px solid #00f5d4;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Main Title
# -------------------------
st.markdown("## 🤖 Gemini AI Chat Assistant")
st.write("Chat seamlessly with Google Gemini models in a smooth, modern interface.")

# -------------------------
# Session State for Chat
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# User Input
# -------------------------
prompt = st.text_area("💬 Your Message:", placeholder="Type your question here...")

if st.button("🚀 Generate Response"):
    if client is None:
        st.error("❌ Gemini client is not initialized. Provide a valid API key in the sidebar.")
    elif not prompt.strip():
        st.warning("⚠️ Please enter a prompt.")
    else:
        with st.spinner("✨ Generating response..."):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                answer = response.text

                # Save conversation
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.messages.append({"role": "bot", "content": answer})

            except Exception as e:
                st.error(f"🔥 Error from Gemini API: {e}")

# -------------------------
# Chat Display
# -------------------------
st.markdown("### 💭 Conversation")
for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "bot"
    st.markdown(
        f"<div class='chat-bubble {role_class}'>{msg['content']}</div>",
        unsafe_allow_html=True
    )
