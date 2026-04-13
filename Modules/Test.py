import streamlit as st
import cv2
import numpy as np
import os
import time

# --- METRIC FUNCTIONS ---

def calculate_laplacian_variance(frame):
    """Measures the sharpness of the image (Blur detection)."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def calculate_snr(frame):
    """Estimates Signal-to-Noise Ratio."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float64)
    mean = np.mean(gray)
    std = np.std(gray)
    if std == 0: return 0
    return 20 * np.log10(mean / std)

def get_video_metadata(path):
    """Extracts resolution and estimates bitrate."""
    cap = cv2.VideoCapture(path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    
    # Estimate bitrate (File size / duration)
    file_size_bits = os.path.getsize(path) * 8
    duration = frame_count / fps if fps > 0 else 0
    bitrate_kbps = (file_size_bits / duration) / 1000 if duration > 0 else 0
    
    cap.release()
    return width, height, fps, bitrate_kbps

# --- UI LAYOUT ---

st.title("🛡️ Pipeline 1: Forensic Triage Engine")
st.markdown("---")

uploaded_file = st.file_uploader("Upload Evidence Video", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Save temp file for OpenCV access
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Video Preview")
        st.video(temp_path)
        
    if st.button("🔍 Evaluate Forensic Metrics"):
        with st.spinner("Analyzing Video Matrix..."):
            # 1. Physical Checks
            w, h, fps, br = get_video_metadata(temp_path)
            
            # 2. Frame-level Analysis (Sample middle frame for speed)
            cap = cv2.VideoCapture(temp_path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_FRAME_COUNT) // 2)
            ret, frame = cap.read()
            
            if ret:
                blur_score = calculate_laplacian_variance(frame)
                snr_score = calculate_snr(frame)
                
                # 3. Calculate FQS (Forensic Quality Score)
                # Weights: w1(Res/100), w2(Bitrate/500), w3(Blur Penalty)
                w1, w2, w3 = 1.0, 0.5, 0.05
                fqs = (w1 * (h)) + (w2 * br) - (w3 * blur_score)
                
                with col2:
                    st.subheader("Metric Evaluation Results")
                    
                    # Display metrics in a clean grid
                    m_col1, m_col2 = st.columns(2)
                    m_col1.metric("Resolution", f"{w}x{h}", delta=f"{h}p")
                    m_col2.metric("Bitrate", f"{br:.2f} kbps")
                    
                    m_col3, m_col4 = st.columns(2)
                    m_col3.metric("Laplacian (Sharpness)", f"{blur_score:.2f}")
                    m_col4.metric("SNR (Purity)", f"{snr_score:.2f} dB")
                    
                    st.markdown("---")
                    st.subheader(f"FQS Score: {fqs:.2f}")
                    
                    if fqs < 600: # Example Threshold
                        st.error("🚨 CRITICAL: Low Quality Detected. Routing to Pipeline 2 (Upscaling).")
                        if st.button("Proceed to Forensic VSR"):
                            st.session_state.target_video = temp_path
                    else:
                        st.success("✅ SUFFICIENT: Quality meets investigation standards.")

            cap.release()
    
    # Clean up (optional: you might want to keep it for the next module)
    # os.remove(temp_path)