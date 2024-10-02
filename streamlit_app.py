import streamlit as st

pg = st.navigation([
    st.Page("Portal.py", title="Dashboard (डैशबोर्ड/ડેશબોર્ડ)", icon="🖥️"),
    st.Page("Chat.py", title="Chat (एआई चैटबॉट/એઆઇ ચેટબોટ)", icon="🤖"),
])

pg.run()