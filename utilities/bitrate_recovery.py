import cv2

def recover_bitrate_artifacts(frame, strength=5):
    # Reduces macroblocking artifacts using a Bilateral Filter.
    # Strength: Diameter of each pixel neighborhood.
    # d: Diameter, sigmaColor: Filter sigma in the color space, sigmaSpace: Filter sigma in coordinate space
    # High sigmaColor helps smooth out blocky compression artifacts
    
    recovered = cv2.bilateralFilter(frame, d=strength, sigmaColor=75, sigmaSpace=75)
    return recovered