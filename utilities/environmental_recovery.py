import cv2
import numpy as np

def apply_retinex_relighting(frame, sigma=100):
    # Simplified Multi-Scale Retinex logic to boost shadows.I = R * L -> R = I / L
    
    img_float = frame.astype(np.float64) + 1.0
    
    # Estimate illumination (L) using Gaussian Blur
    blur = cv2.GaussianBlur(img_float, (0, 0), sigma)
    
    # Log domain transformation for reflectance (R)
    retinex = np.log10(img_float) - np.log10(blur)
    
    # Normalize back to 0-255
    retinex = (retinex - np.min(retinex)) / (np.max(retinex) - np.min(retinex)) * 255.0
    return retinex.astype(np.uint8)

def remove_atmospheric_veil(frame):
    # Simple Contrast Limited Adaptive Histogram Equalization (CLAHE) to remove fog/haze 'veils'.
    
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl,a,b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)