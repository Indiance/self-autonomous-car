#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


def gstreamer_pipeline(sensor_id, width, height, framerate, flip_method):
    return (
        f"nvarguscamerasrc sensor-id={sensor_id} ! "
        f"video/x-raw(memory:NVMM), width=(int){width}, height=(int){height}, "
        f"framerate=(fraction){framerate}/1 ! "
        f"nvvidconv flip-method={flip_method} ! "
        f"video/x-raw, format=(string)BGRx ! "
        f"videoconvert ! "
        f"video/x-raw, format=(string)BGR ! appsink drop=1 max-buffers=1"
    )


class CsiCameraPublisher(Node):
    def __init__(self):
        super().__init__('csi_camera_publisher')

        self.declare_parameter('sensor_id', 0)
        self.declare_parameter('width', 1280)
        self.declare_parameter('height', 720)
        self.declare_parameter('framerate', 30)
        self.declare_parameter('flip_method', 0)
        self.declare_parameter('frame_id', 'csi_camera')
        self.declare_parameter('topic', 'camera/image_raw')

        sensor_id = self.get_parameter('sensor_id').value
        width = self.get_parameter('width').value
        height = self.get_parameter('height').value
        framerate = self.get_parameter('framerate').value
        flip_method = self.get_parameter('flip_method').value
        self.frame_id = self.get_parameter('frame_id').value
        topic = self.get_parameter('topic').value

        pipeline = gstreamer_pipeline(sensor_id, width, height, framerate, flip_method)
        self.get_logger().info(f'Opening CSI camera:\n{pipeline}')

        self.cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
        if not self.cap.isOpened():
            raise RuntimeError(
                'Could not open CSI camera. Check the ribbon cable connection and '
                'that the nvargus-daemon service is running (systemctl status nvargus-daemon).'
            )

        self.bridge = CvBridge()
        self.publisher_ = self.create_publisher(Image, topic, 10)

        period = 1.0 / framerate if framerate > 0 else 1.0 / 30.0
        self.timer = self.create_timer(period, self.timer_callback)

        self.get_logger().info(f'Publishing camera frames on "{topic}" at {framerate} fps')

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warn('Failed to read frame from camera')
            return

        msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self.frame_id
        self.publisher_.publish(msg)

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = CsiCameraPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
