
### Running ORBSLAM2

- if gpu doesnt work, install nvidia-container-runtime and redo
- add docker to group and give permish to user to prevent running on sudo everytime.


xhost + && docker run -it \
--gpus all \
--ipc=host --net=host --privileged \
-e DISPLAY=unix$DISPLAY \
-v /tmp/.X11-unix:/tmp/.X11-unix:rw \
-v /home/praveen/dev/slam/warpsight/ORBSLAM_container:/home/storage/ \
-e NVIDIA_DRIVER_CAPABILITIES=all \
celinachild/orbslam2 /bin/bash


```
./Examples/Monocular/mono_tum Vocabulary/ORBvoc.txt /home/storage/schenley.yaml /home/storage/data/schenley_p1
```


## ORB Slam 3

https://hub.docker.com/r/lmwafer/orb-slam-3-ready

```
xhost +local:root &&  sudo docker run --privileged --name orb-3-container \
--rm -p 8087:8087 -e DISPLAY=$DISPLAY -e QT_X11_NO_MITSHM=1 \
-v /tmp/.X11-unix:/tmp/.X11-unix -v /dev:/dev:ro \
-v /home/praveen/dev/slam/warpsight/ORBSLAM_container:/dpds/storage/ \
-it lmwafer/orb-slam-3-ready:1.0-ubuntu18.04 
```

```
./Examples/Monocular/mono_tum Vocabulary/ORBvoc.txt /dpds/storage/schenley.yaml /dpds/storage/data/schenley_p1

./Examples/Monocular/mono_euroc Vocabulary/ORBvoc.txt /home/storage/GX010035/monocular_EuRoC.yaml /dpds/storage/GX010035
```


<!-- EUROC -->
./Monocular/mono_euroc ../Vocabulary/ORBvoc.txt /dpds/storage/GX010035/monocular_EuRoC.yaml /dpds/storage/GX010035/ /dpds/storage/GX010035/timestamps/

cp CameraTrajectory.txt /dpds/storage/GX010035/Results/Trajectories/CameraTrajectories/optical_flow.txt && cp KeyFrameTrajectory.txt /dpds/storage/GX010035/Results/Trajectories/KeyframeTrajectories/optical_flow.txt

./Monocular-Inertial/mono_inertial_euroc ../Vocabulary/ORBvoc.txt /dpds/storage/GX010040/mono_inertial_EuRoC.yaml /dpds/storage/GX010040/ /dpds/storage/GX010040/timestamps/30fps.txt