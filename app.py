import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Groq AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 Groq AI Chatbot")
st.write("Chat with an AI assistant powered by Groq")

# Get API key from Streamlit Secrets
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant. Give clear and simple answers."
        }
    ]

# Display previous messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# User input
prompt = st.chat_input("Ask me anything...")

if prompt:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    # Get Groq response
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=st.session_state.messages
        )

        answer = response.choices[0].message.content

        # Add assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        with st.chat_message("assistant"):
            st.write(answer)

    except Exception as e:
        st.error(f"Error: {e}")
