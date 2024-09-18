import os
from openai import AzureOpenAI, OpenAI
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
# Utility function to ensure the logs directory exists
def ensure_log_directory_exists():
    if not os.path.exists('logs'):
        os.makedirs('logs')

ensure_log_directory_exists()

st.title("💬   Help")
st.caption("🚀  Get steps ")

ctx = get_script_run_ctx()
session_id = ctx.session_id if ctx else 'unknown_session'

# Initialize session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Function to log the conversation 
def log_conversation(session_id, messages):
    log_file = f'logs/chat_{session_id}.txt'
    with open(log_file, 'w') as f:
        for msg in messages:
            f.write(f"{msg['role']}: {msg['content']}\n")

# Respond to new input
if prompt := st.chat_input():
    #if not st.session_state.get("openai_api_key"):
    #    st.info("Please add your OpenAI API key to continue.")
    #    st.stop()

    #openai_api_key = st.session_state.get("openai_api_key")
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    with open('txt.txt', 'r') as f:
        assistant_msg = f.read()
    response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": f'Answer using following context only: ```{assistant_msg}```'}] +  st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
