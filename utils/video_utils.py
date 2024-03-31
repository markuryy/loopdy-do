import cv2
import numpy as np
from PIL import Image
from models.feature_extractor import FeatureExtractor

def find_loop_segments(video_path, min_distance=5, similarity_threshold=0.9, top_n=5, express_mode=False, progress_callback=None):
    feature_extractor = FeatureExtractor()
    cap = cv2.VideoCapture(video_path)
    features_list = []
    frame_ids = []
    frame_id = 0
    frame_skip = 2 if express_mode else 1
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_id % frame_skip == 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            features = feature_extractor.extract_features(frame_rgb)
            features_list.append(features)
            frame_ids.append(frame_id / cap.get(cv2.CAP_PROP_FPS))
        frame_id += 1
        if progress_callback:
            progress = int(frame_id / total_frames * 100)
            progress_callback(progress)
    cap.release()

    best_pairs = []
    for i in range(len(features_list)):
        for j in range(i + min_distance, len(features_list)):
            cos_sim = np.dot(features_list[i], features_list[j]) / (np.linalg.norm(features_list[i]) * np.linalg.norm(features_list[j]))
            if cos_sim >= similarity_threshold:
                best_pairs.append((frame_ids[i], frame_ids[j], cos_sim))

    best_pairs = sorted(best_pairs, key=lambda x: -x[2])[:top_n]
    return [(start, end) for start, end, _ in best_pairs]

def extract_and_save_loop_segment(video_path, start_time, end_time, output_path, target_fps=None):
    input_video = cv2.VideoCapture(video_path)
    fps = input_video.get(cv2.CAP_PROP_FPS)
    if target_fps is None:
        target_fps = fps
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)
    total_frames = end_frame - start_frame

    input_video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(output_path, fourcc, target_fps, (int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    for _ in range(total_frames):
        ret, frame = input_video.read()
        if not ret:
            break
        output_video.write(frame)

    input_video.release()
    output_video.release()

def create_loop_gif(video_path, start_time, end_time, output_path, target_fps=20, max_dimension=800):
    input_video = cv2.VideoCapture(video_path)
    fps = input_video.get(cv2.CAP_PROP_FPS)
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)
    total_frames = end_frame - start_frame

    input_video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    frames = []
    for _ in range(total_frames):
        ret, frame = input_video.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(Image.fromarray(frame))

    input_video.release()

    # Downscale frames
    width, height = frames[0].size
    if width > height:
        new_width = min(width, max_dimension)
        new_height = int(height * (new_width / width))
    else:
        new_height = min(height, max_dimension)
        new_width = int(width * (new_height / height))
    frames = [frame.resize((new_width, new_height), Image.LANCZOS) for frame in frames]

    # Save as GIF
    frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=1000//target_fps, loop=0)