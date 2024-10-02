import os
from openai import AzureOpenAI, OpenAI
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx

hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Utility function to ensure the logs directory exists
def ensure_log_directory_exists():
    if not os.path.exists('logs'):
        os.makedirs('logs')

ensure_log_directory_exists()

st.sidebar.title("Language Settings")
language = st.sidebar.selectbox("Select Language", ["English", "Hindi", "Gujarati"])

# Track the previously selected language
if "prev_language" not in st.session_state:
    st.session_state["prev_language"] = language

# Check if language has changed
if st.session_state["prev_language"] != language:
    st.session_state["prev_language"] = language
    del st.session_state['messages']

if language == "English":
    st.markdown(f"<h1 style='text-align: center;'>{'Welcome to Jan Seva Kendra Patdi.'}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: left;'>{'📄  Services'}</h3>", unsafe_allow_html=True)
elif language == "Hindi":
    st.markdown(f"<h1 style='text-align: center;'>{'जन सेवा केंद्र पातड़ी में आपका स्वागत है.'}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: left;'>{'📄  सेवाएं'}</h3>", unsafe_allow_html=True)
elif language == "Gujarati":
    st.markdown(f"<h1 style='text-align: center;'>{'જન સેવા કેન્દ્ર પાટડીમાં આપનું સ્વાગત છે.'}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: left;'>{'📄  સેવાઓ'}</h3>", unsafe_allow_html=True)

ctx = get_script_run_ctx()
session_id = ctx.session_id if ctx else 'unknown_session'

# Initialize session state if it doesn't exist
if "messages" not in st.session_state:
    if language == "English":
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    elif language == "Hindi":
        st.session_state["messages"] = [{"role": "assistant", "content": "मैं आपकी कैसे मदद कर सकता हूँ?"}]
    elif language == "Gujarati":
        st.session_state["messages"] = [{"role": "assistant", "content": "હું તમને કેવી રીતે મદદ કરી શકું?"}]

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Function to log the conversation
def log_conversation(session_id, messages):
    log_file = f'logs/chat_{session_id}.txt'
    with open(log_file, 'w') as f:
        for msg in messages:
            f.write(f"{msg['role']}: {msg['content']}\n")

if prompt := st.chat_input():
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    with open('data/txt.txt', 'r') as f:
        assistant_msg = f.read()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": f'You are a Gujarat Govt assistant which just answer the user (peoples) query based on the context provided to you in the language {language} Answer using following context only: ```{assistant_msg}```'}] + st.session_state.messages
    )
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)