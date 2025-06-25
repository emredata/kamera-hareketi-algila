import cv2
import numpy as np
from typing import List

def detect_significant_movement(frames: List[np.ndarray], movement_threshold: float = 10.0) -> List[int]:
    movement_indices = []
    orb = cv2.ORB_create(500)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    for i in range(1, len(frames)):
        prev_gray = cv2.cvtColor(frames[i-1], cv2.COLOR_RGB2GRAY)
        curr_gray = cv2.cvtColor(frames[i], cv2.COLOR_RGB2GRAY)

        kp1, des1 = orb.detectAndCompute(prev_gray, None)
        kp2, des2 = orb.detectAndCompute(curr_gray, None)

        if des1 is None or des2 is None:
            continue

        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)

        if len(matches) < 10:
            continue

        src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1,1,2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        if M is None:
            continue

        dx = M[0,2]
        dy = M[1,2]
        dist = np.sqrt(dx*dx + dy*dy)

        if dist > movement_threshold:
            movement_indices.append(i)

    return movement_indices
