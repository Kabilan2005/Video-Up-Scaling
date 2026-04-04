import cv2
import os
from utilities.resolution_engine import get_video_characteristics
from utilities.calculate_metrics import calculate_laplacian_variance, calculate_snr
from utilities.fqs_calculator import compute_fqs

class ForensicQualityCheck:
    def __init__(self, video_path):
        self.video_path = video_path

    def run_full_analysis(self):
        """
        Performs the forensic triage and returns a dictionary of results.
        Returns None or an error dict if the file cannot be processed.
        """
        # 1. Extracting Quality metrics
        chars = get_video_characteristics(self.video_path)
        if not chars:
            return {"error": "Failed to extract video characteristics."}
        
        # 2. Frame-level Analysis 
        cap = cv2.VideoCapture(self.video_path)
        ret, frame = cap.read()
        
        if not ret:
            cap.release()
            return {"error": "Failed to read video frame."}
        
        blur = calculate_laplacian_variance(frame)
        snr = calculate_snr(frame)
        cap.release()
        
        # 3. Decision Matrix (Using 2.0 Mbps as a sample baseline)
        fqs = compute_fqs(chars['height'], 2.0, blur)
        
        threshold = 50.0
        action = "PROCEED TO PIPELINE 2" if fqs < threshold else "SUFFICIENT QUALITY"
        
        # --- THE FIX: Return a dictionary for the UI to read ---
        return {
            "fqs": round(fqs, 2),
            "resolution": chars['label'],
            "dimensions": f"{chars['width']}x{chars['height']}",
            "blur": round(blur, 2),
            "snr": round(snr, 2),
            "bitrate": 2.0,
            "action": action,
            "needs_upscale": fqs < threshold
        }