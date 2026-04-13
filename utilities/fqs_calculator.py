def compute_fqs(resolution_h, bitrate_mbps, blur_var, weights=(0.4, 0.4, 0.2)):
    """
    FQS = (w1 * Resolution) + (w2 * Bitrate) - (w3 * Blur_Penalty)
    Weights are based on how it affects the quality in forensics.
    Note: We normalize values to a 0-100 scale for consistency.
    """
    w1, w2, w3 = weights
    
    # Normalized components (simple linear mapping for example)
    res_score = min(resolution_h / 1080 * 100, 100)
    br_score = min(bitrate_mbps / 10 * 100, 100)
    blur_penalty = min(blur_var / 500 * 100, 100) # Assuming 500 is very sharp
    
    fqs = (w1 * res_score) + (w2 * br_score) - (w3 * (100 - blur_penalty))
    return round(fqs, 2)