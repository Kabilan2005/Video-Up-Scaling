import streamlit as st
from streamlit_option_menu import option_menu
from UI import home_page, investigation_page

st.set_page_config(page_title="Forensic VSR System", layout="wide", initial_sidebar_state="collapsed")

# 2. Advanced CSS Injection
# We force the container to the very front (z-index: 1000) and add a backdrop-filter 
# z-index used to control the order of stacking of the UI elements. along the z-axis perpendicular to the screen
st.markdown("""
    <style>
        .nav-wrapper {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #0E1117;
            z-index: 1000;
            border-top: 1px solid #333;
            padding: 5px 0;
        }
        /* Create padding at the bottom of the page so content isn't hidden by the nav */
        .main .block-container {
            padding-bottom: 100px;
        }
    </style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = "Home"

# 4. Define the Navigation Function
def render_nav():
    st.markdown('<div class="nav-wrapper">', unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None,
        options=["Home", "Investigation", "Techniques", "Export"],
        icons=["house", "camera-reels", "cpu", "download"],
        menu_icon="cast",
        default_index=["Home", "Investigation", "Techniques", "Exoprt"].index(st.session_state.page),
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#FF4B4B", "font-size": "18px"}, 
            "nav-link": {"font-size": "14px", "text-align": "center", "margin":"0px", "--hover-color": "#262730"},
            "nav-link-selected": {"background-color": "#FF4B4B", "color": "white"},
        }
    )
    st.markdown('</div>', unsafe_allow_html=True)
    return selected

# 5. EXECUTION FLOW
# We handle the navigation selection FIRST to prevent "flicker"
selected_page = render_nav()

if selected_page != st.session_state.page:
    st.session_state.page = selected_page
    st.rerun()

if st.session_state.page == "Home":
    home_page.show()
elif st.session_state.page == "Investigation":
    investigation_page.show()
elif st.session_state.page == "Techniques":
    techniques_page.show()
elif st.session_state.page == "Export":
    export_page.show()