import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="Gen AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Title
st.title("🤖 Gen AI Chatbot")
st.write("Chat with an AI powered by Groq")

# Groq API
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# Store conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User input
prompt = st.chat_input("Type your message here...")

if prompt:

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Send conversation to Groq
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=st.session_state.messages
    )

    # Get AI response
    answer = response.choices[0].message.content

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(answer)

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
