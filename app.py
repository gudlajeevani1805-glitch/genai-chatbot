!pip install groq gradio gtts

import os
from getpass import getpass

os.environ["GROQ_API_KEY"] = getpass("Enter your Groq API Key: ")

from groq import Groq
from gtts import gTTS
import os

client = Groq(
    api_key=os.environ["GROQ_API_KEY"]
)


def voice_chat(audio, history):

    if audio is None:
        return history, None

    # 🎤 Voice to Text
    with open(audio, "rb") as file:

        transcription = client.audio.transcriptions.create(
            file=file,
            model="whisper-large-v3-turbo"
        )

    user_text = transcription.text

    # 🤖 Prepare conversation
    messages = [
        {
            "role": "system",
            "content": "You are a friendly and helpful AI voice assistant."
        }
    ]

    # Add previous messages
    for user_message, ai_message in history:

        messages.append({
            "role": "user",
            "content": user_message
        })

        messages.append({
            "role": "assistant",
            "content": ai_message
        })

    # Add current question
    messages.append({
        "role": "user",
        "content": user_text
    })

    # 🤖 Groq AI
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    ai_text = response.choices[0].message.content

    # 🔊 Text to Speech
    tts = gTTS(
        text=ai_text,
        lang="en"
    )

    output_file = "ai_response.mp3"

    tts.save(output_file)

    # Save conversation
    history.append(
        (user_text, ai_text)
    )

    return history, output_file

import gradio as gr


with gr.Blocks(
    title="Groq AI Voice Chatbot"
) as demo:

    gr.Markdown(
        """
        # 🤖 Groq AI Voice Chatbot

        ### 🎤 Speak with your AI assistant
        """
    )

    chatbot = gr.Chatbot(
        label="Conversation"
    )

    microphone = gr.Audio(
        sources=["microphone"],
        type="filepath",
        label="🎤 Speak"
    )

    response_audio = gr.Audio(
        label="🔊 AI Response",
        autoplay=True
    )

    clear_button = gr.Button(
        "🗑️ Clear Chat"
    )

    microphone.change(
        voice_chat,
        inputs=[
            microphone,
            chatbot
        ],
        outputs=[
            chatbot,
            response_audio
        ]
    )

    clear_button.click(
        lambda: ([], None),
        outputs=[
            chatbot,
            response_audio
        ]
    )


demo.launch(
    share=True
)
