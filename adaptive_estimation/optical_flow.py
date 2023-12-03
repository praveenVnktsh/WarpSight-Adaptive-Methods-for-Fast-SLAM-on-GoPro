import cv2
import glob
import numpy as np
import imageio
import av
import os
from tqdm import tqdm

os.makedirs('data/videos', exist_ok=True)
feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

video_path = '/home/praveenvnktsh/dev/slam_proj/warpsight/data/videos/schenley_p1.mp4'
container = av.open(video_path)
stream = container.streams.video[0]

root = video_path.replace('videos/', "").replace('.mp4', '/')
os.makedirs(root + 'frames', exist_ok=True)
f = open(root + 'data.txt', 'w')

frames_to_skip = 0
cur_frame = None
prev_frame = None

image_idx = 0
total_frames = int(stream.duration * stream.time_base * stream.framerate)
downscale_ratio = 0.7
pbar = tqdm(container.decode(video = 0), total=total_frames)
for frame in pbar:
    image_idx += 1
    if frames_to_skip > 0:
        frames_to_skip -= 1
        prev_frame = np.array(frame.to_image())
        prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        prev_frame = cv2.resize(prev_frame, (0, 0), fx = downscale_ratio, fy = downscale_ratio)
        continue
    
    cur_frame = np.array(frame.to_image())
    og_frame = cur_frame.copy()
    cur_frame = cv2.cvtColor(cur_frame, cv2.COLOR_BGR2GRAY)
    cur_frame = cv2.resize(cur_frame, (0, 0), fx = downscale_ratio, fy = downscale_ratio)
    if prev_frame is None:
        prev_frame = cur_frame
        continue
    p0 = cv2.goodFeaturesToTrack(cur_frame, mask=None, **feature_params)
    p1, st, err = cv2.calcOpticalFlowPyrLK(prev_frame, cur_frame, p0, None, **lk_params)
    
    good_new = p1[st == 1]
    good_old = p0[st == 1]
    
    viz_frame = prev_frame.copy()
    viz_frame = cv2.cvtColor(viz_frame, cv2.COLOR_GRAY2BGR)
    dists = []
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        c, d = old.ravel()
        
        dist = np.sqrt((a - c)**2 + (b - d)**2)
        dists.append(dist)
        a = int(a)
        b = int(b)
        c = int(c)
        d = int(d)
        
        viz_frame = cv2.line(viz_frame, (a, b), (c, d), (0, 255, 0), 2)
        viz_frame = cv2.circle(viz_frame, (a, b), 5, (0, 0, 255), -1)
    
    mean_disp = np.mean(dists)
    frame_rate = max(1, min(240, (mean_disp * 240/50)))
    frames_to_skip = int(240/frame_rate)
    frames_to_skip = min(max(1, frames_to_skip), 100)
    
    timestamp = float(frame.pts * stream.time_base)
    pbar.set_description("Skipping {} frames. Timestamp: {}".format(frames_to_skip, timestamp))
    
    write_path = 'frames/' + str(image_idx).zfill(8) + '.jpg'
    f.write(str(timestamp) + '\t' + write_path + '\n')
    cv2.imwrite(root + write_path, og_frame[:, :, ::-1])
    cv2.imshow('Optical Flow', cv2.resize(viz_frame, (0, 0), fx = 0.5, fy = 0.5))
    if cv2.waitKey(1) == ord('q'):  # Press 'Esc' to exit
        break
f.close()