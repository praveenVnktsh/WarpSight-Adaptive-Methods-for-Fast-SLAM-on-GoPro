
### Running ORBSLAM2

- if gpu doesnt work, install nvidia-container-runtime and redo
- add docker to group and give permish to user to prevent running on sudo everytime.


xhost + && docker run -it \
--gpus all \
--ipc=host --net=host --privileged \
-e DISPLAY=unix$DISPLAY \
-v /tmp/.X11-unix:/tmp/.X11-unix:rw \
-v /home/praveenvnktsh/dev/slam_proj/warpsight/ORBSLAM_container:/home/storage/ \
-e NVIDIA_DRIVER_CAPABILITIES=all \
praveenvnktsh001/warpsight:update /bin/bash


```
./Examples/Monocular/mono_tum Vocabulary/ORBvoc.txt /home/storage/schenley.yaml /home/storage/data/schenley_p1
```


## ORB Slam 3

https://hub.docker.com/r/lmwafer/orb-slam-3-ready

```
xhost +local:root && docker run --privileged --name orb-3-container \
--rm -p 8087:8087 -e DISPLAY=$DISPLAY -e QT_X11_NO_MITSHM=1 \
-v /tmp/.X11-unix:/tmp/.X11-unix -v /dev:/dev:ro \
-v /home/praveenvnktsh/dev/slam_proj/warpsight/ORBSLAM_container:/dpds/storage/ \
--gpus all -it lmwafer/orb-slam-3-ready:1.0-ubuntu18.04
```

```
./Examples/Monocular/mono_tum Vocabulary/ORBvoc.txt /dpds/storage/schenley.yaml /dpds/storage/data/schenley_p1
```