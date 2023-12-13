import cv2
import glob
import numpy as np
from tqdm import tqdm
import glob
import os
feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

root = '/home/praveen/dev/slam/warpsight/ORBSLAM_container/GX010035/'
f = open(root + 'optical_flow.txt', 'w')

frames_to_skip = 0
cur_frame = None
prev_frame = None

image_idx = 0
image_idx = 0
paths = list(sorted(glob.glob('/home/praveen/dev/slam/warpsight/ORBSLAM_container/GX010035/mav0/cam0/data/*.png')))
pbar = tqdm(enumerate(paths), total = len(paths))
for image_idx, filename in pbar:
    
    cur_frame = cv2.imread(filename, 0)
    if cur_frame is None:
        break
    
    if prev_frame is None:
        prev_frame = cur_frame
        continue
    try:
        p0 = cv2.goodFeaturesToTrack(cur_frame, mask=None, **feature_params)
        p1, st, err = cv2.calcOpticalFlowPyrLK(prev_frame, cur_frame, p0, None, **lk_params)
        
        good_new = p1[st == 1]
        good_old = p0[st == 1]
        
        mean_disp = np.mean(
            np.linalg.norm(good_new - good_old, axis = 1)
        )
    except:
        mean_disp = 100
    viz_frame = prev_frame.copy()
    viz_frame = cv2.cvtColor(viz_frame, cv2.COLOR_GRAY2BGR)
    # mean_disp = np.mean(dists)
    name = os.path.basename(filename)
    f.write(name + '\t' +  str(mean_disp) + '\n')
    image_idx += 1

f.close()