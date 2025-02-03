import streamlit as st
import requests

# Set page title
st.set_page_config(page_title="DeepSeek AI Chat", layout="centered")

# Title
st.title("💬 DeepSeek AI Chat - Powered by DeepInfra")

# API Details
API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {st.secrets['PAT']}"  # Store API Key securely in Streamlit Secrets
}

# Initialize conversation history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are a helpful and knowledgeable assistant."}
    ]

# Function to query DeepInfra API
def query_model(user_input):
    # Append user input to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Prepare payload
    payload = {
        "model": "deepseek-ai/DeepSeek-R1",
        "messages": st.session_state.chat_history,
        "max_tokens": 600  # Limit response length
    }

    # Send request
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    # Process response
    if response.status_code == 200:
        ai_response = response.json()["choices"][0]["message"]["content"]
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        return ai_response
    else:
        return f"⚠️ Error {response.status_code}: {response.text}"

# Display chat history
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"**You:** {chat['content']}")
    elif chat["role"] == "assistant":
        st.markdown(f"**AI:** {chat['content']}")

# User input box
user_input = st.text_input("Enter your message:", key="input")

# Send button
if st.button("Send"):
    if user_input:
        response = query_model(user_input)
        st.experimental_rerun()  # Refresh chat history
