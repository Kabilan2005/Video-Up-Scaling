import streamlit as st
import os
from pipelines.quality_check import ForensicQualityCheck

def show():
    st.markdown(f"### 📹 Video Analysis: {st.session_state.get('current_case', 'General')}")
    
    # Layout: Video (Left) | Metrics (Right)
    col_vid, col_met = st.columns([2, 1])

    with col_vid:
        uploaded_file = st.file_uploader("Upload Evidence", type=['mp4', 'avi'])
        
        if uploaded_file:
            temp_path = f"data/{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.video(temp_path)
            
            st.info("💡 Tip: Use the 'Select ROI' tool below to focus on a Face or Plate.")
            # Note: ROI/Crop tool will be integrated here in the next module

    with col_met:
        st.markdown("#### 📊 Forensic Metrics")
        if uploaded_file:
            with st.spinner("Analyzing Frame Quality..."):
                # CALLING THE PIPELINE
                checker = ForensicQualityCheck(temp_path)
                results = checker.run_full_analysis()
                
                st.metric("Forensic Quality Score (FQS)", f"{results['fqs']}/100")
                st.write(f"**Resolution:** {results['resolution']}")
                st.write(f"**Bitrate:** {results['bitrate']} Mbps")
                
                if results['fqs'] < 50:
                    st.error("⚠️ Quality: INSUFFICIENT")
                    if st.button("🚀 Deploy Forensic VSR (Pipeline 2)"):
                        st.session_state.page = "Techniques"
                        st.rerun()
                else:
                    st.success("✅ Quality: FORENSICALLY SOUND")
                    st.button("💾 Save to Case Book")
        else:
            st.write("Upload a video to see metrics.")