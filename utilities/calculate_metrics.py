import cv2
import numpy as np

def calculate_laplacian_variance(frame):
    # Measures sharpness. High = Sharp, Low = Blurry.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def calculate_snr(frame):
    # Measures Signal-to-Noise Ratio. High = Clean, Low = Grainy.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float64)
    mean_signal = np.mean(gray)
    std_noise = np.std(gray)
    if std_noise == 0: return 100 
    # Perfect signal
    snr = 20 * np.log10(mean_signal / std_noise)
    return snr