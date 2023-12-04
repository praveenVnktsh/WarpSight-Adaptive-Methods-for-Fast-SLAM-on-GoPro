import cv2
import glob
import numpy as np
import imageio
import av
import os
from tqdm import tqdm
from more_itertools import one

os.makedirs('/home/praveenvnktsh/dev/slam_proj/warpsight/ORBSLAM_container/data/videos', exist_ok=True)
feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

video_path = '/home/praveenvnktsh/dev/slam_proj/warpsight/ORBSLAM_container/data/videos/schenley_p1.mp4'
root = video_path.replace('videos/', "").replace('.mp4', '/')
os.makedirs(root + 'frames', exist_ok=True)
f = open(root + 'optical_flow.txt', 'w')

frames_to_skip = 0
cur_frame = None
prev_frame = None

image_idx = 0
image_idx = 0

for image_idx in tqdm(range(43500)):
    
    cur_frame = cv2.imread('/home/praveenvnktsh/dev/slam_proj/warpsight/ORBSLAM_container/data/schenley_p1/frames/' + str(image_idx).zfill(8) + '.jpg', 0)
    if cur_frame is None:
        break
    
    if prev_frame is None:
        prev_frame = cur_frame
        continue

    p0 = cv2.goodFeaturesToTrack(cur_frame, mask=None, **feature_params)
    p1, st, err = cv2.calcOpticalFlowPyrLK(prev_frame, cur_frame, p0, None, **lk_params)
    
    good_new = p1[st == 1]
    good_old = p0[st == 1]
    
    viz_frame = prev_frame.copy()
    viz_frame = cv2.cvtColor(viz_frame, cv2.COLOR_GRAY2BGR)
    mean_disp = np.mean(
        np.linalg.norm(good_new - good_old, axis = 1)
    )

    # mean_disp = np.mean(dists)
    write_path = 'frames/' + str(image_idx).zfill(8) + '.jpg'
    f.write(write_path + '\t' +  str(mean_disp) + '\n')
    image_idx += 1

f.close()