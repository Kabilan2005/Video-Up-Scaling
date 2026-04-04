import cv2
import os
from utilities.resolution_engine import get_video_characteristics
from utilities.quality_metrics import calculate_laplacian_variance, calculate_snr
# from utilities.face_detector import detect_face_confidence
from utilities.fqs_calculator import compute_fqs

def run_triage(video_path):
    print(f"--- Starting Forensic Triage: {os.path.basename(video_path)} ---")
    
    # 1. Extracting Quality metrics like Resolution, Bitrate, FPS, Scale
    chars = get_video_characteristics(video_path)
    
    # 2. Frame-level Analysis 
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if not ret: return "Error reading file"
    
    blur = calculate_laplacian_variance(frame)
    snr = calculate_snr(frame)
    # SNR is kept as a backup - Eliminating Double Counting since Blur_Rate deals with artifacts which in tuen handles cleanliness
    # conf, ai_flag = detect_face_confidence(frame)
    
    # 3. Decision Matrix (Assume 2Mbps for sample calc)
    fqs = compute_fqs(chars['height'], 2.0, blur)
    
    threshold = 50.0
    action = "PROCEED TO PIPELINE 2" if fqs < threshold else "SUFFICIENT QUALITY"
    
    print(f"Results: Res={chars['label']}, FQS={fqs})
    # , Face_Conf={conf:.2f}")
    print(f"Action: {action}")
    
    cap.release()

if __name__ == "__main__":
    # run_triage("data/test_cctv.mp4")
    pass.