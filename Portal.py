import json
import streamlit as st

# Load service data from JSON file
data = json.load(open('data/data.json'))

st.set_page_config('Jan Seva Kendra Patdi', layout="wide", page_icon="assets/images.png")

hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Set page configuration

# Sidebar for language settings
st.sidebar.title("Language Settings")
language = st.sidebar.selectbox("Select Language", ["English", "Hindi", "Gujarati"])

# Depending on the selected language, load the respective JSON file or dictionary
# Note: Ensure you have corresponding translation files or dictionaries
if language == "Hindi":
    # Load Hindi translations
    data = json.load(open('data/data_hindi.json'))
elif language == "Gujarati":
    # Load Gujarati translations
    data = json.load(open('data/data_gujarati.json'))

# pg = st.navigation([
#     st.Page("Chat.py", title="First page", icon="🔥"),
#     st.Page("Portal.py", title="Sco page", icon="🔥"),
# ])

# Main page content
if language == "English":
    st.markdown(f"<h1 style='text-align: center;'>{'Welcome to Jan Seva Kendra Patdi.'}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: left;'>{'📄  Services'}</h3>", unsafe_allow_html=True)
elif language == "Hindi":
    st.markdown(f"<h1 style='text-align: center;'>{'जन सेवा केंद्र पातड़ी में आपका स्वागत है.'}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: left;'>{'📄  सेवाएं'}</h3>", unsafe_allow_html=True)
elif language == "Gujarati":
    st.markdown(f"<h1 style='text-align: center;'>{'જન સેવા કેન્દ્ર પાટડીમાં આપનું સ્વાગત છે.'}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: left;'>{'📄  સેવાઓ'}</h3>", unsafe_allow_html=True)

# Displaying services details
for app, details in data.items():
    with st.expander(f"{app}", expanded=False):
        keys = list(details.keys())
        st.write(f"**{keys[0]}:** {details[keys[0]]}")
        st.write(f"**{keys[1]}:**")
        for doc in details[keys[1]]:
            st.write(f"- {doc}")

