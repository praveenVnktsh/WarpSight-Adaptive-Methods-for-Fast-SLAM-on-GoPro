import numpy as np

with open('/home/praveenvnktsh/dev/slam_proj/warpsight/ORBSLAM_container/data/schenley_p1/optical_flow.txt', 'r') as f:
    lines = f.readlines()
    

for line in lines:
    line = line.strip()
    if len(line) == 0:
        continue
    
    line = line.split('\t')
    path = line[0]
    disp = float(line[1])
    
    frames_to_skip = 0
    