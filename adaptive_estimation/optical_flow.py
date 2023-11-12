import cv2
import glob
import numpy as np
import imageio

feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

j = 0
paths = sorted(glob.glob('/home/praveenvnktsh/warpsight/data/dji/5/*.png'))
final_frames = []
selected_indices = []
image_idx = 0
j = 1
while j < len(paths):
    path = paths[j]
    cur_frame = cv2.imread(path, 0)
    prev_frame = cv2.imread(paths[j - 1], 0)
    
    p0 = cv2.goodFeaturesToTrack(cur_frame, mask=None, **feature_params)
    p1, st, err = cv2.calcOpticalFlowPyrLK(prev_frame, cur_frame, p0, None, **lk_params)
    
    good_new = p1[st == 1]
    good_old = p0[st == 1]
    
    selected_indices.append(j)
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
    
    j += frames_to_skip
    print(j, np.mean(dists),)
    final_frames.append(viz_frame)
    
    cv2.imwrite('outputs/{}.png'.format(str(image_idx).zfill(7)), viz_frame)
    image_idx += 1
    cv2.imshow('Optical Flow', cv2.resize(viz_frame, (0, 0), fx = 0.5, fy = 0.5))
    if cv2.waitKey(1) == ord('q'):  # Press 'Esc' to exit
        break
    j += 1
import json
with open('selected_indics.json', 'w') as f:
    json.dump(selected_indices, f)