import streamlit as st
from streamlit_option_menu import option_menu
from ui import home_page, investigation_page

# Configuring the Page
st.set_page_config(page_title="Forensic VSR", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = "Home"

if st.session_state.page == "Home":
    home_page.show()
elif st.session_state.page == "Investigation":
    investigation_page.show()

# Bottom Navigation Bar
st.markdown("<br><br><br>", unsafe_allow_html=True) 
selected = option_menu(
    menu_title=None,
    options=["Home", "Investigation", "Techniques", "Settings"],
    icons=["house", "camera-reels", "cpu", "gear"],
    orientation="horizontal",
    styles={
        "container": {"position": "fixed", "bottom": "0", "width": "100%", "z-index": "99"}
    }
)

if selected != st.session_state.page:
    st.session_state.page = selected
    st.rerun()