import gpmf

video_path = '/home/praveenvnktsh/dev/slam_proj/warpsight/ORBSLAM_container/data/videos/schenley_p1.mp4'
# Read the binary stream from the file
stream = gpmf.io.extract_gpmf_stream(video_path)

# Extract GPS low level data from the stream
gps_blocks = gpmf.gps.extract_gps_blocks(stream)

# Parse low level data into more usable format
gps_data = list(map(gpmf.gps.parse_gps_block, gps_blocks))
