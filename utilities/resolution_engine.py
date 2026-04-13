import cv2

def get_video_characteristics(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None

    # Physical properties 
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS)
    bitrate = cap.get(cv2.CAP_PROP_BITRATE) 
    # Note: Often returns 0, handled in main
    
    aspect_ratio = round(width / height, 2)
    
    # Logic for True Resolution Check
    resolution_label = f"{height}p"
    if height <= 240: label = "CIF"
    elif height <= 480: label = "D1/Standard"
    else: label = "HD+"

    cap.release()
    return {
        "width": width,
        "height": height,
        "fps": fps,
        "aspect_ratio": aspect_ratio,
        "label": label
    }