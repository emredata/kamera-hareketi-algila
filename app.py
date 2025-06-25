import streamlit as st
import cv2
import numpy as np
import tempfile
import os

def detect_camera_movement_homography(prev_frame, curr_frame, min_matches=20, movement_threshold=8.0):
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(nfeatures=2000)

    kp1, des1 = orb.detectAndCompute(prev_gray, None)
    kp2, des2 = orb.detectAndCompute(curr_gray, None)

    if des1 is None or des2 is None or len(kp1) < min_matches or len(kp2) < min_matches:
        return False, None

    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(des1, des2, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    if len(good_matches) < min_matches:
        return False, None

    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1,1,2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    if M is None or mask is None:
        return False, None

    inliers = np.sum(mask)
    if inliers < len(good_matches) * 0.7:
        return False, None

    dx = M[0,2]
    dy = M[1,2]
    translation_magnitude = np.sqrt(dx*dx + dy*dy)

    movement_detected = translation_magnitude > movement_threshold

    return movement_detected, M

def group_consecutive_frames(frames, min_group_size=3):
    if not frames:
        return []

    grouped = []
    temp_group = [frames[0]]

    for i in range(1, len(frames)):
        if frames[i] == frames[i-1] + 1:
            temp_group.append(frames[i])
        else:
            if len(temp_group) >= min_group_size:
                grouped.extend(temp_group)
            temp_group = [frames[i]]

    if len(temp_group) >= min_group_size:
        grouped.extend(temp_group)

    return grouped

st.title("Kamera Hareketi Algılama Web Uygulaması")

uploaded_file = st.file_uploader("Video yükleyin (MP4, AVI, MOV)", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Geçici dosyaya kaydet
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    st.video(video_path)

    # Parametreler
    min_matches = st.sidebar.slider("Minimum Eşleşme Sayısı", 5, 50, 20)
    movement_threshold = st.sidebar.slider("Hareket Eşiği (piksel)", 1.0, 20.0, 8.0)
    min_group_size = st.sidebar.slider("Minimum Ardışık Hareket Kare Sayısı", 1, 10, 3)

    cap = cv2.VideoCapture(video_path)
    ret, prev_frame = cap.read()
    if not ret:
        st.error("Video açılamadı veya boş.")
        cap.release()
    else:
        movement_frames_raw = []
        frame_idx = 1

        with st.spinner("Hareket algılanıyor..."):
            while True:
                ret, curr_frame = cap.read()
                if not ret:
                    break

                movement_detected, _ = detect_camera_movement_homography(
                    prev_frame, curr_frame,
                    min_matches=min_matches,
                    movement_threshold=movement_threshold
                )

                if movement_detected:
                    movement_frames_raw.append(frame_idx)

                prev_frame = curr_frame
                frame_idx += 1

        cap.release()

        movement_frames = group_consecutive_frames(movement_frames_raw, min_group_size=min_group_size)

        st.write(f"Hareket algılanan kareler (filtrelenmiş): {movement_frames}")

        # İlk 5 hareketli kareyi göster
        display_limit = 5
        displayed_count = 0

        cap = cv2.VideoCapture(video_path)
        for idx in movement_frames:
            if displayed_count >= display_limit:
                break
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), caption=f"Hareket algılanan kare {idx}")
                displayed_count += 1
        cap.release()

        if len(movement_frames) > display_limit:
            st.info(f"Toplam {len(movement_frames)} hareket karesi bulundu. Sadece ilk {display_limit} tanesi gösterildi.")











