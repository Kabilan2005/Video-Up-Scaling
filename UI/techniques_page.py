import streamlit as st
import cv2
import numpy as np
from pipelines.processing_engine import ForensicVSR_Pipeline2

def show():
    st.markdown("### 🛠️ Pipeline 2: Guided Forensic Reconstruction")
    
    # 1. Check if a video was passed from Pipeline 1
    if 'target_video' not in st.session_state:
        st.warning("No video selected. Please complete Pipeline 1 (Triage) first.")
        if st.button("Go to Investigation"):
            st.session_state.page = "Investigation"
            st.rerun()
        return

    # 2. Initialize the Engine State
    if 'step_index' not in st.session_state:
        st.session_state.step_index = 0
        # Load the first frame for preview
        cap = cv2.VideoCapture(st.session_state.target_video)
        ret, frame = cap.read()
        st.session_state.working_frame = frame if ret else None
        st.session_state.original_preview = frame.copy() if ret else None
        st.session_state.choices = {} # To store Yes/No decisions
        cap.release()

    steps = [
        {"name": "Bitrate Recovery", "desc": "Heal macroblocks and compression artifacts."},
        {"name": "Environmental Fix", "desc": "Apply Retinex relighting and De-hazing."},
        {"name": "Denoising", "desc": "Remove sensor grain and thermal noise."},
        {"name": "Spatial Upscaling", "desc": "Increase pixel density (Super-Resolution)."},
        {"name": "Sharpening", "desc": "Final edge refinement for detail extraction."}
    ]

    current_step = steps[st.session_state.step_index]
    
    st.progress((st.session_state.step_index + 1) / len(steps))
    st.subheader(f"Step {st.session_state.step_index + 1}: {current_step['name']}")
    st.info(current_step['desc'])

    col_pre, col_post = st.columns(2)

    # Initialize Engine with the current working frame
    engine = ForensicVSR_Pipeline2(st.session_state.working_frame)

    # Generate the "Expert Candidate" (The YES preview)
    candidate_frame = None
    idx = st.session_state.step_index
    if idx == 0: candidate_frame = engine.step_1_bitrate(apply=True)
    elif idx == 1: candidate_frame = engine.step_2_environment(relight=True, dehaze=True)
    elif idx == 2: candidate_frame = engine.step_3_denoise(apply=True)
    elif idx == 3: candidate_frame = engine.step_4_upscale(factor=2)
    elif idx == 4: candidate_frame = engine.step_5_sharpen(apply=True)

    with col_pre:
        st.caption("Current Matrix State")
        st.image(st.session_state.working_frame, channels="BGR", use_container_width=True)

    with col_post:
        st.caption(f"Candidate: With {current_step['name']}")
        st.image(candidate_frame, channels="BGR", use_container_width=True)

    st.markdown("---")
    c1, c2, c3 = st.columns([1, 1, 2])
    
    if c1.button("✅ Apply (YES)"):
        st.session_state.choices[current_step['name']] = True
        st.session_state.working_frame = candidate_frame # Commit the change
        move_next()

    if c2.button("❌ Skip (NO)"):
        st.session_state.choices[current_step['name']] = False
        # Do not update working_frame; pass the current one forward
        move_next()

def move_next():
    if st.session_state.step_index < 4:
        st.session_state.step_index += 1
        st.rerun()
    else:
        st.session_state.page = "Export" # Move to final gallery
        st.rerun()