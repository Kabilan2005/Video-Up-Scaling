import streamlit as st
import cv2

def show():
    st.markdown("### 🏁 Final Forensic Review")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Evidence")
        st.image(st.session_state.original_preview, channels="BGR")
        
    with col2:
        st.subheader("Enhanced Reconstruction")
        st.image(st.session_state.working_frame, channels="BGR")

    # Display the Audit Trail
    st.markdown("#### 📝 Applied Techniques (Audit Log)")
    for tech, applied in st.session_state.choices.items():
        status = "✅ Applied" if applied else "⚪ Skipped"
        st.write(f"- {tech}: {status}")

    st.markdown("---")
    
    # DOWNLOAD OPTIONS
    st.subheader("📥 Export Evidence")
    d_col1, d_col2 = st.columns(2)
    
    with d_col1:
        st.button("🎥 Download Full Video (.mp4)", use_container_width=True)
        st.caption("High-quality reconstruction for court playback.")
        
    with d_col2:
        st.button("🖼️ Download Frame-by-Frame (.zip)", use_container_width=True)
        st.caption("Individual PNG frames for forensic exhibits.")