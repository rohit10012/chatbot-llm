import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ✅ Configuration Variables
DEFAULT_APP_NAME = "Groq AI Chatbot"  # Change as needed
DEFAULT_MODEL = "llama3-8b-8192"  # Default model
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-api-key-here")  # Load API key from .env or hardcode it

# ✅ Streamlit UI
st.set_page_config(page_title=DEFAULT_APP_NAME, layout="wide")
st.title(st.text_input("Enter your application name:", DEFAULT_APP_NAME))

# ✅ Model Selection
available_models = ["llama3-8b-8192", "mixtral-8x7b", "gemma-7b"]  # Add more as needed
selected_model = st.selectbox("Choose AI Model", available_models, index=0)

# ✅ Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful AI assistant."}]

# ✅ Chat Input
user_input = st.text_area("Your Message", placeholder="Ask something...")

# ✅ API Request Function
def query_groq_api(messages):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": selected_model,
        "messages": messages
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# ✅ Send Message
if st.button("Send"):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Thinking..."):
            response = query_groq_api(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # ✅ Display chat history
        for msg in st.session_state.messages:
            if msg["role"] != "system":
                st.write(f"**{msg['role'].capitalize()}**: {msg['content']}")
    else:
        st.warning("Please enter a message.")

# ✅ Clear Chat History Button
if st.button("Clear Chat"):
    st.session_state.messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
    st.success("Chat history cleared.")