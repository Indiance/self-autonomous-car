# car_vision

CSI camera capture for the RC car, built on `nvarguscamerasrc` (Jetson Argus ISP) via GStreamer + OpenCV, published as a standard `sensor_msgs/Image` topic.

## Build

```bash
cd ~/Desktop/self_autonomous_car
source /opt/ros/humble/setup.bash
colcon build --symlink-install --packages-select car_vision
source install/setup.bash
```

## Run — publisher only

```bash
ros2 run car_vision csi_camera_publisher
```

Publishes `bgr8` frames on `/camera/image_raw` at 30 fps, 1280x720 by default.

Parameters (`--ros-args -p name:=value`): `sensor_id`, `width`, `height`, `framerate`, `flip_method` (0-7, rotate/flip the image if the camera is mounted upside down), `frame_id`, `topic`.

## View the feed

Option A — this package's viewer window (needs a display; run with `DISPLAY=:1` if viewing on the Jetson's own screen):

```bash
ros2 run car_vision image_viewer
```

Press `q` in the window to quit.

Option B — rqt:

```bash
ros2 run rqt_image_view rqt_image_view
```

Option C — launch file (publisher + viewer together):

```bash
ros2 launch car_vision camera.launch.py view:=true
```

## Notes

- Requires the `nvargus-daemon` systemd service to be running (`systemctl status nvargus-daemon`) — it owns the CSI camera on Jetson.
- Only one process can hold the Argus camera at a time; stop the publisher before running raw `gst-launch-1.0`/`nvgstcapture` tests against the same camera.
- Next step for object detection/avoidance: subscribe to `/camera/image_raw` from a new node and run inference there (e.g. TensorRT/YOLO), rather than modifying this publisher.
