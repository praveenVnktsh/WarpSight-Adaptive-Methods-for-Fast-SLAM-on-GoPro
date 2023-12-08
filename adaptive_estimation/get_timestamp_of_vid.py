import av
from tqdm import tqdm
from more_itertools import one
import numpy as np

video_path = '/home/praveenvnktsh/dev/slam_proj/warpsight/ORBSLAM_container/data/videos/schenley_p1.mp4'
container = av.open(video_path)
stream = container.streams.video[0]
stream = one(container.streams.video)
ctx_gpu = av.Codec('hevc_cuvid', 'r').create()
ctx_gpu.extradata = stream.codec_context.extradata
pbar = tqdm(container.demux(stream), total=43000)

for packet in pbar:
    for frame in ctx_gpu.decode(packet):
        time_since_start = float(frame.pts * stream.time_base)
        unix_time = 1591042800 + time_since_start
        print(frame.pts)