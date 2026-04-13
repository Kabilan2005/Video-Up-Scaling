import streamlit as st
import os
from pipelines.quality_check import ForensicQualityCheck

def show():
    st.markdown(f"### 📹 Video Analysis: {st.session_state.get('current_case', 'General Investigation')}")
    st.markdown("---")
    
    # Layout: Video (Left) | Metrics (Right)
    col_vid, col_met = st.columns([2, 1])

    if not os.path.exists("data"):
        os.makedirs("data")

    with col_vid:
        uploaded_file = st.file_uploader("Upload Evidence", type=['mp4', 'avi', 'mkv'])
        
        if uploaded_file:
            temp_path = os.path.join("data", uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.video(temp_path)
            st.info("💡 Tip: Use the 'Select ROI' tool (Module 3) to focus on specific evidence.")

    with col_met:
        st.markdown("#### 📊 Forensic Triage Report")
        
        if uploaded_file:
            with st.spinner("Analyzing Frame Quality..."):
                # 1. Initialize the Pipeline Class
                checker = ForensicQualityCheck(temp_path)
                
                # 2. Run Analysis and get the Dictionary
                results = checker.run_full_analysis()
                
                # 3. Safety Check: Display results only if they exist
                if results and "error" not in results:
                    st.session_state.target_video = temp_path
                    st.metric("Forensic Quality Score (FQS)", f"{results['fqs']}/100")
                    
                    with st.expander("Detailed Metrics", expanded=True):
                        st.write(f"**Resolution:** {results['resolution']} ({results['dimensions']})")
                        st.write(f"**Bitrate:** {results['bitrate']} Mbps")
                        st.write(f"**Sharpness:** {results['blur']}")
                    
                    if results['needs_upscale']:
                        st.error(f"**Decision:** {results['action']}")
                        if st.button("🚀 Deploy Forensic VSR", use_container_width=True):
                            st.session_state.page = "Techniques"
                            st.rerun()
                    else:
                        st.success(f"**Decision:** {results['action']}")
                        st.button("💾 Save to Case Book", use_container_width=True)
                else:
                    st.error(results.get("error", "Unknown Error in Pipeline"))
        else:
            st.write("Upload a video to see metrics.")