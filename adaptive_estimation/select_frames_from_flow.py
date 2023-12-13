import numpy as np



with open('/home/praveen/dev/slam/warpsight/ORBSLAM_container/GX010040/optical_flow.txt', 'r') as f:

    

    data = f.readlines()

num_frames = len(data)
f = open('/home/praveen/dev/slam/warpsight/ORBSLAM_container/GX010040/timestamps/timestamps_optical_flow.txt', 'w')

ts = []
disps = []
for line in data:
    name, disp = line.split('\t')
    disp = float(disp)
    ts.append(name)
    disps.append(disp)

disps = np.array(disps)
disps = np.nan_to_num(disps)
disps /= disps.max()
disps = 1 - disps

max_frames_to_skip = 15
i = 0
while i < len(disps):
    f.write(ts[i].split('.')[0] + '\n')
    if i < 3600:
        frames_to_skip = 8
    else:
        frames_to_skip = int((disps[i]) * max_frames_to_skip ) + 1
    print(disps[i], frames_to_skip)

    i += frames_to_skip

