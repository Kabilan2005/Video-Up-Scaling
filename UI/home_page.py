import streamlit as st

def show():
    st.markdown("### 📖 Case Management System")
    st.write("Select an investigation book to begin triage.")

    # Grid for Case Books
    cols = st.columns(3)
    
    cases = [
        {"id": "2026-DL-01", "loc": "New Delhi", "status": "Active", "color": "blue"},
        {"id": "2026-MB-05", "loc": "Mumbai", "status": "Pending", "color": "orange"},
        {"id": "2026-KA-09", "loc": "Bengaluru", "status": "Completed", "color": "green"}
    ]

    for i, case in enumerate(cases):
        with cols[i % 3]:
            with st.container(border=True):
                st.subheader(case['id'])
                st.caption(f"📍 {case['loc']}")
                st.progress(100 if case['status'] == "Completed" else 40)
                if st.button(f"Open Case", key=f"btn_{case['id']}"):
                    st.session_state.current_case = case['id']
                    st.session_state.page = "Investigation"
                    st.rerun()