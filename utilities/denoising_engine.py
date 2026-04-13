import cv2

def apply_denoising(frame, method="median", h=10):
    
    # h: Parameter regulating filter strength. Higher h value perfectly removes noise but also removes image details.
    if method == "median":
        # Best for Salt and Pepper noise
        return cv2.medianBlur(frame, 5)
    else:
        return cv2.fastNlMeansDenoisingColored(frame, None, h, h, 7, 21)