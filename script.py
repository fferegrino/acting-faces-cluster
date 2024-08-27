from scenedetect import detect, ContentDetector, split_video_ffmpeg


path = '/Users/antonioferegrino/Movies/movies/ullozhukku/Ullozhukku - Trailer _ Parvathy Thiruvothu, Urvashi _ Christo Tomy _ Sushin Shyam _ 21 June 2024.mp4' 

scenes = detect(path, ContentDetector())

# Print scene list
for i, scene in enumerate(scenes):
    print(f'Scene {i+1}: Start {scene[0].get_seconds()}, End {scene[1].get_seconds()}')
