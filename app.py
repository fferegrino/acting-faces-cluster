import streamlit as st
from scenedetect import detect, ContentDetector, split_video_ffmpeg
import cv2
from ultralytics import YOLO
from collections import defaultdict
import face_recognition
from sklearn.cluster import DBSCAN

from matplotlib import pyplot as plt

def detect_faces(frame, confidence=0.5):
    results = model(frame, verbose=False)
    detections = results[0].boxes.data.cpu().numpy()

    res = []
    for det in detections:
        x1, y1, x2, y2, conf, class_id = det
        if results[0].names[int(class_id)] == 'Human face':
            if conf > confidence:
                res.append(det)
            
    return res

model = YOLO('yolov5s_face_relu6.pt')

video_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
temp_video_path = "temp_video.mp4"

if video_file is not None:
    video_bytes = video_file.read()
    # st.video(video_bytes)

    # Save the video to a temporary file
    with open(temp_video_path, "wb") as f:
        f.write(video_bytes)

    # Perform scene detection
    scenes = detect(temp_video_path, ContentDetector())

    video = cv2.VideoCapture(temp_video_path)
    # st.write(scenes)

    face_id = 0
    scene_faces = defaultdict(list)
    detected_faces = []
    frames = []
    encodings = []
    face_id_scene = {}
    for scene_id, scene in enumerate(scenes):
        video.set(cv2.CAP_PROP_POS_FRAMES, scene[0].get_frames())
        ret, frame = video.read()
        frames.append(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
        detections = detect_faces(frame)
        for detection in detections:
            x1, y1, x2, y2, *_ = detection
            scene_faces[scene_id].append(face_id)
            detected_faces.append(detection)
            [encoding] = face_recognition.face_encodings(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB), [(int(y1), int(x2), int(y2), int(x1))])
            encodings.append(encoding)
            face_id_scene[face_id] = scene_id
            face_id += 1

    col1, col2 = st.columns(2)

    with col1:
        eps = st.slider('Epsilon', min_value=0.0, max_value=1.0, value=0.45)
    with col2:
        min_samples = st.slider('Min samples', min_value=1, max_value=10, value=3)

    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(encodings)  

    face_clusters = defaultdict(list)
    for i, label in enumerate(clustering.labels_):
        if label != -1:  # -1 is noise
            face_clusters[label].append(i)

    for cluster_id, face_ids in face_clusters.items():
        fig, axs = plt.subplots(1,5, figsize=(50, 10))
        for ax, fid in zip(axs, face_ids[:10]):
            ax.imshow(frames[face_id_scene[fid]])

        st.pyplot(fig)