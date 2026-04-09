import cv2
import numpy as np

def upscale_video_frame(frame, scale_factor=2):

    height, width = frame.shape[:2]
    new_size = (width * scale_factor, height * scale_factor)
    return cv2.resize(frame, new_size, interpolation=cv2.INTER_CUBIC)

def apply_sharpening(frame):
    
    # Matrix: Sharp = Original + (Original - Blurred) * Amount
 
    gaussian_3 = cv2.GaussianBlur(frame, (0, 0), 2.0)
    # Highlight the edges by subtracting the blur from the original
    
    sharpened = cv2.addWeighted(frame, 1.5, gaussian_3, -0.5, 0)
    return sharpened