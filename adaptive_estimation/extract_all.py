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
container = av.open(video_path)
stream = container.streams.video[0]

root = video_path.replace('videos/', "").replace('.mp4', '/')
os.makedirs(root + 'frames', exist_ok=True)
f = open(root + 'rgb.txt', 'w')

frames_to_skip = 0
cur_frame = None
prev_frame = None

image_idx = 0
total_frames = int(stream.duration * stream.time_base * stream.framerate)
downscale_ratio = 1

stream = one(container.streams.video)
ctx_gpu = av.Codec('hevc_cuvid', 'r').create()
ctx_gpu.extradata = stream.codec_context.extradata
pbar = tqdm(container.demux(stream), total=43000)
image_idx = 0
for packet in pbar:
    for frame in ctx_gpu.decode(packet):
        cur_frame = np.array(frame.to_image())[:, :, ::-1]
        
        timestamp = float(frame.pts * stream.time_base)
        pbar.set_description("Skipping {} frames. Timestamp: {}".format(frames_to_skip, timestamp))
        
        write_path = 'frames/' + str(image_idx).zfill(8) + '.jpg'
        f.write(str(timestamp) + '\t' + write_path + '\n')
        cv2.imwrite(root + write_path, cur_frame)
        # cv2.imshow('Optical Flow', cv2.resize(cur_frame, (0, 0), fx = 0.5, fy = 0.5))
        image_idx += 1
        if timestamp > 180:
            break
        if cv2.waitKey(1) == ord('q'):  
            break
f.close()